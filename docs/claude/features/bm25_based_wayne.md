# BM25_Wayne Search System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a **new, separate** search system `BM25_Wayne`. **Wayne and all its existing functions, endpoints, and behaviour are untouched.** BM25_Wayne uses BM25 (instead of TF-IDF) for its text component in coarse search, keeps HOG/EHD/CLD visual features, and has the full Wayne-style personalization, explanations, and comparison pipeline. All changes are purely additive.

**Architecture:** Add a `get_all_scores()` method to `BM25Baseline` that returns min-max normalized BM25 scores for all documents. Add a new coarse search function `comics_coarse_search_bm25_wayne()` in `coarse_search.py` (alongside the existing `comics_coarse_search()` — the existing function is not modified). Add a utility wrapper and two new FastAPI endpoints. Frontend registers the new system in constants, navbar, and About Us table.

**Tech Stack:** Python/FastAPI backend, rank_bm25, NumPy, React 18/MUI frontend

**Phase 2 (future, not in this plan):** Reduce title/genre repetition weights in `bm25_search.py::build_book_text()` and ingest per-book OCR text from `python_backend_api/data/metadata/COMICS_ocr_file.csv` to reduce title/genre bias.

---

## File Map

| File | Change |
|------|--------|
| `python_backend_api/search/coarse/bm25_search.py` | Add `get_all_scores()` to `BM25Baseline` |
| `python_backend_api/search/coarse/coarse_search.py` | Add import + `comics_coarse_search_bm25_wayne()` |
| `python_backend_api/fastapi_webserver/coarse_search_utils.py` | Add `perform_bm25_wayne_coarse_search()` |
| `python_backend_api/fastapi_webserver/search_main.py` | Add `/book_search_with_bm25_wayne` and `/book_search_with_bm25_wayne_searchbar` |
| `react_frontend_ui/src/components/constants.js` | Add `BM25_Wayne` to `SYSTEMS_TO_API_ENDPOINT_MAPPING` |
| `react_frontend_ui/src/components/navbar.js` | Add `<MenuItem value="BM25_Wayne">` |
| `react_frontend_ui/src/pages/AboutUs.js` | Add table row for `BM25_Wayne` |

---

## Task 1: Add `get_all_scores()` to BM25Baseline

**Files:**
- Modify: `python_backend_api/search/coarse/bm25_search.py`

`BM25Baseline.retrieve()` currently returns top-N ranked indices only. The hybrid coarse search needs a full-length normalized score array so it can combine with visual feature cosine similarities via weighted addition.

- [ ] **Step 1: Add the method**

In `python_backend_api/search/coarse/bm25_search.py`, insert the following method after `get_pseudo_query()` (after line 122, before `retrieve()`):

```python
    def get_all_scores(self, query_book_idx: int) -> np.ndarray:
        """Min-max normalized BM25 scores for all documents given a query book.

        Returns a 1-D float64 array of length n_docs with values in [0, 1].
        The query book's own score is zeroed out to avoid self-retrieval.
        Used by the BM25_Wayne hybrid coarse search.
        """
        pseudo_query = self.get_pseudo_query(query_book_idx)
        if not pseudo_query:
            return np.zeros(len(self.metadata_df), dtype=np.float64)

        raw_scores = self.bm25.get_scores(pseudo_query).copy()
        raw_scores[query_book_idx] = 0.0  # exclude self

        min_score = raw_scores.min()
        max_score = raw_scores.max()
        if max_score - min_score < 1e-10:
            return np.zeros_like(raw_scores, dtype=np.float64)
        return ((raw_scores - min_score) / (max_score - min_score)).astype(np.float64)
```

- [ ] **Step 2: Smoke test from Python REPL**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api
python - <<'EOF'
import sys
sys.path.insert(0, '.')
from search.coarse.bm25_search import bm25_engine
import numpy as np

scores = bm25_engine.get_all_scores(650)   # Batman book
print("shape:", scores.shape)
print("min:", scores.min(), "max:", scores.max())
print("self score (idx 650):", scores[650])  # should be 0.0
assert scores.shape[0] > 1000
assert scores.min() >= 0.0 and scores.max() <= 1.0
assert scores[650] == 0.0
print("OK")
EOF
```

Expected:
```
shape: (1712,)
min: 0.0  max: 1.0
self score (idx 650): 0.0
OK
```

- [ ] **Step 3: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add python_backend_api/search/coarse/bm25_search.py
git commit -m "feat(bm25): add get_all_scores() for hybrid coarse search"
```

---

## Task 2: Add hybrid coarse search function

**Files:**
- Modify: `python_backend_api/search/coarse/coarse_search.py`

Add a new function `comics_coarse_search_bm25_wayne()` — `comics_coarse_search()` is **not modified**. The new function has the same structure but uses BM25 `get_all_scores()` for the text term instead of `text_tfidf` cosine similarity.

Note: `utils.cosine_similarity(A, B)` returns an `(N, 1)` matrix. BM25 `get_all_scores()` returns `(N,)`. Reshape to `(N, 1)` before combining.

- [ ] **Step 1: Add import at top of coarse_search.py**

After the line `import common_constants.backend_constants as cst` in `python_backend_api/search/coarse/coarse_search.py`, add:

```python
from search.coarse import bm25_search
```

- [ ] **Step 2: Add the hybrid search function**

Append the following function at the end of `python_backend_api/search/coarse/coarse_search.py` (before `if __name__ == "__main__":`):

```python
def comics_coarse_search_bm25_wayne(
    query_comic_book_id: int, feature_weight_dict: dict, top_n: int
):
    """Coarse search for BM25_Wayne: BM25 text scores + HOG/EHD/CLD visual features.

    Identical pipeline to comics_coarse_search() but replaces the TF-IDF text
    cosine similarity term with min-max normalized BM25 scores from bm25_engine.
    """
    query_book_id = query_comic_book_id

    # Visual feature cosine similarities (same as Wayne)
    cld_cosine_similarity = utils.cosine_similarity(
        cld_tfidf_np[:, :], cld_tfidf_np[max(query_book_id, 0) : query_book_id + 1, :]
    )
    edh_cosine_similarity = utils.cosine_similarity(
        edh_tfidf_np[:, :], edh_tfidf_np[max(query_book_id, 0) : query_book_id + 1, :]
    )
    hog_cosine_similarity = utils.cosine_similarity(
        hog_tfidf_np[:, :], hog_tfidf_np[max(query_book_id, 0) : query_book_id + 1, :]
    )
    comic_cover_img_cosine_similarity = utils.cosine_similarity(
        comic_cover_img_np[:, :],
        comic_cover_img_np[max(query_book_id, 0) : query_book_id + 1, :],
    )
    comic_cover_txt_cosine_similarity = utils.cosine_similarity(
        comic_cover_txt_np[:, :],
        comic_cover_txt_np[max(query_book_id, 0) : query_book_id + 1, :],
    )

    # BM25 text scores replacing TF-IDF text cosine similarity
    raw_bm25_scores = bm25_search.bm25_engine.get_all_scores(query_book_id)  # shape (N,)
    bm25_text_scores = raw_bm25_scores.reshape(-1, 1)  # shape (N, 1) to match cosine sim matrices

    # Weighted combination (text weight applies to BM25 scores)
    combined_results_similarity = (
        cld_cosine_similarity * feature_weight_dict["cld"]
        + edh_cosine_similarity * feature_weight_dict["edh"]
        + hog_cosine_similarity * feature_weight_dict["hog"]
        + bm25_text_scores * feature_weight_dict["text"]
        + comic_cover_img_cosine_similarity * feature_weight_dict["comic_img"]
        + comic_cover_txt_cosine_similarity * feature_weight_dict["comic_txt"]
    )

    combined_results_indices = np.argsort(
        np.squeeze(-combined_results_similarity), axis=0
    )
    combined_sorted_result_indices = np.sort(-combined_results_similarity, axis=0)

    top_k_df = get_top_n_matching_book_info(
        idx_top_n_np=combined_results_indices,
        sim_score_top_n_np=combined_sorted_result_indices,
        comic_info_dict=book_metadata_dict,
        print_n=top_n,
        query_book_id=query_book_id,
        feature_similarity_type="coarse_combined_bm25_wayne",
    )
    return top_k_df
```

- [ ] **Step 3: Smoke test from Python REPL**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api
python - <<'EOF'
import sys
sys.path.insert(0, '.')
from search.coarse.coarse_search import comics_coarse_search_bm25_wayne

feature_weight_dict = {"cld": 0.1, "edh": 0.1, "hog": 0.1, "text": 1.7, "comic_img": 1.0, "comic_txt": 1.0}
df = comics_coarse_search_bm25_wayne(query_comic_book_id=650, feature_weight_dict=feature_weight_dict, top_n=21)
print(df[["rank", "comic_no", "book_title", "genre"]].head(10))
assert len(df) >= 10
assert 650 not in df["comic_no"].values, "query book should not appear in results"
print("OK")
EOF
```

Expected: 10 rows of comic books (not including book 650).

- [ ] **Step 4: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add python_backend_api/search/coarse/coarse_search.py
git commit -m "feat(search): add comics_coarse_search_bm25_wayne() hybrid coarse search"
```

---

## Task 3: Add coarse search utility wrapper

**Files:**
- Modify: `python_backend_api/fastapi_webserver/coarse_search_utils.py`

Add `perform_bm25_wayne_coarse_search()` following the same pattern as `perform_coarse_search()` (lines 19–52).

- [ ] **Step 1: Add the function**

Append the following function at the end of `python_backend_api/fastapi_webserver/coarse_search_utils.py` (after `perform_bm25_text_search()`):

```python
def perform_bm25_wayne_coarse_search(
    b_id: int,
    feature_weight_dict={
        "cld": 0.1,
        "edh": 0.1,
        "hog": 0.1,
        "text": 1.7,
        "comic_img": 1.0,
        "comic_txt": 1.0,
    },
    top_n=200,
):
    """BM25_Wayne hybrid coarse search: BM25 text scores + HOG/EHD/CLD visual features."""
    top_n_results_df = coarse_search.comics_coarse_search_bm25_wayne(
        query_comic_book_id=b_id, feature_weight_dict=feature_weight_dict, top_n=top_n
    )
    coarse_filtered_book_df = top_n_results_df[
        ["comic_no", "book_title", "genre", "year"]
    ]
    coarse_filtered_book_df.fillna("", inplace=True)
    coarse_filtered_book_lst = coarse_filtered_book_df.to_dict("records")
    coarse_filtered_book_new_lst = []
    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        coarse_filtered_book_new_lst.append(d)
    print(f"BM25_Wayne QBE Query Book: {b_id}")
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)
```

- [ ] **Step 2: Smoke test from Python REPL**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api
python - <<'EOF'
import sys
sys.path.insert(0, '.')
sys.path.insert(1, 'fastapi_webserver')
from coarse_search_utils import perform_bm25_wayne_coarse_search

lst, df = perform_bm25_wayne_coarse_search(b_id=650, top_n=200)
print(f"results count: {len(lst)}")
print(lst[:2])
assert len(lst) > 10
assert all("comic_no" in d for d in lst[:5])
print("OK")
EOF
```

Expected: list of ~200 dicts with `comic_no`, `book_title`, `genre`, `year`, `id` keys.

- [ ] **Step 3: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add python_backend_api/fastapi_webserver/coarse_search_utils.py
git commit -m "feat(search): add perform_bm25_wayne_coarse_search() utility"
```

---

## Task 4: Add FastAPI endpoints

**Files:**
- Modify: `python_backend_api/fastapi_webserver/search_main.py`

Add two endpoints mirroring Wayne's, using `cs_utils.perform_bm25_wayne_coarse_search()` for QBE. Both keep the full Wayne pipeline: adaptive facet weight learning via `rrr`, interpretable reranking via `is_utils`, and intelligent explanation via `erf.explain_relevance_feedback()` (not the random variant). Free-text queries fall back to `cs_utils.perform_bm25_text_search()`.

- [ ] **Step 1: Add `/book_search_with_bm25_wayne` endpoint**

In `search_main.py`, insert after the `/book_search_with_bm25` endpoint (after line 1421):

```python
@app.post("/book_search_with_bm25_wayne", status_code=200)
async def search_with_bm25_wayne_qbe(
    cbl: BookList,
    b_id: int = Query(...),
    generate_fake_clicks: bool = Query(default=True),
    input_feature_importance_dict: Optional[FacetWeight] = FacetWeight(
        gender=1.0,
        supersense=1.0,
        genre_comb=1.0,
        panel_ratio=1.0,
        comic_cover_img=1.0,
        comic_cover_txt=1.0,
    ),
):
    (
        coarse_filtered_book_new_lst,
        coarse_filtered_book_df,
    ) = cs_utils.perform_bm25_wayne_coarse_search(b_id=b_id)

    global book_search_results_history_lst

    if generate_fake_clicks:
        clicksinfo_dict = create_fake_clicks_for_previous_timestep_data(
            coarse_filtered_book_df=coarse_filtered_book_df
        )
    else:
        clicksinfo_dict = create_real_clicks_for_previous_timestamp_data(
            cbl.interested_book_lst
        )

    if not generate_fake_clicks:
        if utils.check_if_hovered(
            clicksinfo_dict=clicksinfo_dict, b_id=b_id
        ) and not utils.check_if_all_books_are_hovered(
            clicksinfo_dict=clicksinfo_dict, b_id=b_id
        ):
            (
                feature_importance_dict,
                normalized_feature_importance_dict,
                clf_coef,
            ) = rrr.adapt_facet_weights_from_previous_timestep_click_info_triplet_loss(
                previous_click_info_lst=clicksinfo_dict, query_book_id=b_id
            )
        else:
            normalized_feature_importance_dict = {
                "gender": input_feature_importance_dict.gender,
                "supersense": input_feature_importance_dict.supersense,
                "genre_comb": input_feature_importance_dict.genre_comb,
                "panel_ratio": input_feature_importance_dict.panel_ratio,
                "comic_cover_img": input_feature_importance_dict.comic_cover_img,
                "comic_cover_txt": input_feature_importance_dict.comic_cover_txt,
            }
            clf_coef = None
            feature_importance_dict = normalized_feature_importance_dict
        clf_coef = None
        feature_importance_dict = normalized_feature_importance_dict
    else:
        normalized_feature_importance_dict = {
            "gender": input_feature_importance_dict.gender,
            "supersense": input_feature_importance_dict.supersense,
            "genre_comb": input_feature_importance_dict.genre_comb,
            "panel_ratio": input_feature_importance_dict.panel_ratio,
            "comic_cover_img": input_feature_importance_dict.comic_cover_img,
            "comic_cover_txt": input_feature_importance_dict.comic_cover_txt,
        }
        clf_coef = None
        feature_importance_dict = normalized_feature_importance_dict

    (
        interpretable_filtered_book_lst,
        interpretable_filtered_book_df,
        historical_book_ids_lst,
    ) = is_utils.adaptive_rerank_coarse_search_results(
        normalized_feature_importance_dict=normalized_feature_importance_dict,
        query_comic_book_id=b_id,
        coarse_search_results_lst=coarse_filtered_book_new_lst,
        top_k=20,
        historical_book_ids_lst=book_search_results_history_lst.copy(),
    )

    book_search_results_history_lst = historical_book_ids_lst.copy()

    if generate_fake_clicks:
        relevance_feedback_explanation_dict = await erf.explain_relevance_feedback(
            clicksinfo_dict=[],
            query_book_id=b_id,
            search_results=interpretable_filtered_book_lst,
            model=sentence_transformer_model,
        )
    else:
        relevance_feedback_explanation_dict = await erf.explain_relevance_feedback(
            clicksinfo_dict=clicksinfo_dict,
            query_book_id=b_id,
            search_results=interpretable_filtered_book_lst,
            model=sentence_transformer_model,
        )

    interpretable_filtered_book_new_lst = [
        interpretable_filtered_book_lst.copy(),
        normalized_feature_importance_dict,
        relevance_feedback_explanation_dict,
    ]

    global latest_session_folderpath
    utils.log_session_data(
        latest_session_folderpath,
        {
            "input_data": {
                "cbl": cbl.dict(),
                "b_id": b_id,
                "generate_fake_clicks": generate_fake_clicks,
                "input_feature_importance_dict": input_feature_importance_dict.dict(),
            },
            "output_data": {
                "interpretable_filtered_book_new_lst": interpretable_filtered_book_new_lst
            },
            "function_name": "search_with_bm25_wayne_qbe",
        },
    )
    return interpretable_filtered_book_new_lst
```

- [ ] **Step 2: Add `/book_search_with_bm25_wayne_searchbar` endpoint**

Append after `/book_search_with_bm25_wayne`:

```python
@app.post("/book_search_with_bm25_wayne_searchbar", status_code=200)
async def search_with_bm25_wayne_searchbar(
    searchbar_query: SearchBarQuery,
    input_feature_importance_dict: Optional[FacetWeight] = FacetWeight(
        gender=1.0,
        supersense=1.0,
        genre_comb=1.0,
        panel_ratio=1.0,
        comic_cover_img=1.0,
        comic_cover_txt=1.0,
    ),
):
    print("searchbar_query (BM25_Wayne): {}".format(searchbar_query))

    global book_search_results_history_lst
    book_search_results_history_lst = []

    if (
        searchbar_query.type == "book"
        or searchbar_query.type == "character"
        or searchbar_query.type == "genre"
    ):
        b_id = searchbar_query.comic_no
        (
            coarse_filtered_book_new_lst,
            coarse_filtered_book_df,
        ) = cs_utils.perform_bm25_wayne_coarse_search(b_id=b_id)
    elif searchbar_query.type == "free text":
        (
            coarse_filtered_book_new_lst,
            coarse_filtered_book_df,
        ) = cs_utils.perform_bm25_text_search(query_text=searchbar_query.text, top_n=19)
        b_id = coarse_filtered_book_new_lst[0]["comic_no"] if coarse_filtered_book_new_lst else 1
    else:
        b_id = 1
        (
            coarse_filtered_book_new_lst,
            coarse_filtered_book_df,
        ) = cs_utils.perform_bm25_wayne_coarse_search(b_id=b_id)

    is_free_text_query = searchbar_query.type == "free text"

    if is_free_text_query:
        normalized_feature_importance_dict = {
            "gender": 1.0, "supersense": 1.0, "genre_comb": 1.0,
            "panel_ratio": 1.0, "comic_cover_img": 1.0, "comic_cover_txt": 1.0,
        }
    else:
        normalized_feature_importance_dict = {
            "gender": input_feature_importance_dict.gender,
            "supersense": input_feature_importance_dict.supersense,
            "genre_comb": input_feature_importance_dict.genre_comb,
            "panel_ratio": input_feature_importance_dict.panel_ratio,
            "comic_cover_img": input_feature_importance_dict.comic_cover_img,
            "comic_cover_txt": input_feature_importance_dict.comic_cover_txt,
        }

    if is_free_text_query:
        interpretable_filtered_book_lst = coarse_filtered_book_new_lst
        relevance_feedback_explanation_dict = await erf.explain_relevance_feedback_at_random(
            clicksinfo_dict=[],
            query_book_id=b_id,
            search_results=interpretable_filtered_book_lst,
            model=sentence_transformer_model,
        )
    else:
        (
            interpretable_filtered_book_lst,
            interpretable_filtered_book_df,
            historical_book_ids_lst,
        ) = is_utils.adaptive_rerank_coarse_search_results(
            normalized_feature_importance_dict=normalized_feature_importance_dict,
            query_comic_book_id=b_id,
            coarse_search_results_lst=coarse_filtered_book_new_lst,
            top_k=20,
            historical_book_ids_lst=book_search_results_history_lst.copy(),
        )
        book_search_results_history_lst = historical_book_ids_lst.copy()
        relevance_feedback_explanation_dict = await erf.explain_relevance_feedback(
            clicksinfo_dict=[],
            query_book_id=b_id,
            search_results=interpretable_filtered_book_lst,
            model=sentence_transformer_model,
        )

    interpretable_filtered_book_new_lst = [
        interpretable_filtered_book_lst.copy(),
        normalized_feature_importance_dict,
        relevance_feedback_explanation_dict,
    ]

    global latest_session_folderpath
    utils.log_session_data(
        latest_session_folderpath,
        {
            "input_data": {
                "searchbar_query": searchbar_query.dict(),
                "input_feature_importance_dict": input_feature_importance_dict.dict(),
            },
            "output_data": {
                "interpretable_filtered_book_new_lst": interpretable_filtered_book_new_lst
            },
            "function_name": "search_with_bm25_wayne_searchbar",
        },
    )
    return interpretable_filtered_book_new_lst
```

- [ ] **Step 3: Verify endpoint registration**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api/fastapi_webserver
uvicorn search_main:app --port 8001 &
SERVER_PID=$!
sleep 15
curl -s http://localhost:8001/openapi.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
paths = list(data['paths'].keys())
assert '/book_search_with_bm25_wayne' in paths, 'missing endpoint'
assert '/book_search_with_bm25_wayne_searchbar' in paths, 'missing searchbar endpoint'
print('Routes OK:', [p for p in paths if 'bm25_wayne' in p])
"
kill $SERVER_PID
```

Expected:
```
Routes OK: ['/book_search_with_bm25_wayne', '/book_search_with_bm25_wayne_searchbar']
```

- [ ] **Step 4: Test book-click endpoint with curl**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api/fastapi_webserver
uvicorn search_main:app --port 8001 &
SERVER_PID=$!
sleep 15
curl -s -X POST "http://localhost:8001/book_search_with_bm25_wayne?b_id=650&generate_fake_clicks=true" \
  -H "Content-Type: application/json" \
  -d '{"interested_book_lst": []}' | python3 -c "
import json, sys
data = json.load(sys.stdin)
assert isinstance(data, list) and len(data) == 3, 'expected [results, weights, explanations]'
results, weights, explanations = data
assert len(results) > 0, 'no results'
assert 'gender' in weights, 'missing facet weights'
assert results[0].get('book_title'), 'missing book_title'
print(f'Results count: {len(results)}, first: {results[0][\"book_title\"]}')
print('facet weights:', weights)
print('OK')
"
kill $SERVER_PID
```

Expected: 3-element response with >0 results and real facet weights.

- [ ] **Step 5: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add python_backend_api/fastapi_webserver/search_main.py
git commit -m "feat(api): add /book_search_with_bm25_wayne and /book_search_with_bm25_wayne_searchbar endpoints"
```

---

## Task 5: Register BM25_Wayne in frontend constants

**Files:**
- Modify: `react_frontend_ui/src/components/constants.js`

- [ ] **Step 1: Add the BM25_Wayne entry**

In `react_frontend_ui/src/components/constants.js`, find the closing brace and comma of the `BM25` entry:

```javascript
  BM25: {
    search_bar: "http://localhost:8000/book_search_with_bm25_searchbar",
    book_grid: "http://localhost:8000/book_search_with_bm25?b_id=",
    local_explanation: "http://localhost:8000/local_explanation",
    comparision: "http://localhost:8000/compare_books",
    relevance_feedback: "",
    view_pdf: "http://localhost:8000/view_comic_book/",
  },
```

After it, add:

```javascript
  BM25_Wayne: {
    search_bar: "http://localhost:8000/book_search_with_bm25_wayne_searchbar",
    book_grid: "http://localhost:8000/book_search_with_bm25_wayne?b_id=",
    local_explanation: "http://localhost:8000/local_explanation",
    comparision: "http://localhost:8000/compare_books",
    relevance_feedback: "",
    view_pdf: "http://localhost:8000/view_comic_book/",
  },
```

- [ ] **Step 2: Verify**

```bash
grep -n "BM25_Wayne" react_frontend_ui/src/components/constants.js
```

Expected: at least 1 hit.

- [ ] **Step 3: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add react_frontend_ui/src/components/constants.js
git commit -m "feat(frontend): register BM25_Wayne system in constants.js"
```

---

## Task 6: Add BM25_Wayne to navbar dropdown

**Files:**
- Modify: `react_frontend_ui/src/components/navbar.js`

- [ ] **Step 1: Add MenuItem**

In `react_frontend_ui/src/components/navbar.js`, find:

```jsx
          <MenuItem value="BM25">BM25</MenuItem>
```

Replace with:

```jsx
          <MenuItem value="BM25">BM25</MenuItem>
          <MenuItem value="BM25_Wayne">BM25_Wayne</MenuItem>
```

- [ ] **Step 2: Verify**

```bash
grep -n "BM25_Wayne" react_frontend_ui/src/components/navbar.js
```

Expected: 1 hit.

- [ ] **Step 3: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add react_frontend_ui/src/components/navbar.js
git commit -m "feat(frontend): add BM25_Wayne to navbar system dropdown"
```

---

## Task 7: Add BM25_Wayne row to AboutUs page

**Files:**
- Modify: `react_frontend_ui/src/pages/AboutUs.js`

- [ ] **Step 1: Add the table row**

In `react_frontend_ui/src/pages/AboutUs.js`, find the closing `</tr>` of the BM25 row (the row with `className="row-bm25"`). Insert the following row immediately after it:

```jsx
              <tr className="row-bm25-wayne">
                <td><strong>BM25_Wayne</strong></td>
                <td>BM25, CLD, EHD, HOG</td>
                <td>✅ Adaptive</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>BM25 text + visual features + full Wayne personalization</td>
              </tr>
```

- [ ] **Step 2: Verify**

```bash
grep -n "BM25_Wayne" react_frontend_ui/src/pages/AboutUs.js
```

Expected: 1 hit.

- [ ] **Step 3: Commit**

```bash
cd /home/ss/IdeaProjects/personal/escomic
git add react_frontend_ui/src/pages/AboutUs.js
git commit -m "feat(frontend): add BM25_Wayne row to About Us systems table"
```

---

## Task 8: End-to-end verification

- [ ] **Step 1: Start backend**

```bash
cd /home/ss/IdeaProjects/personal/escomic/python_backend_api/fastapi_webserver
uvicorn search_main:app --port 8000 --reload
```

Confirm server starts without import errors. Check logs for `[BM25] Index ready` message.

- [ ] **Step 2: Start frontend**

```bash
cd /home/ss/IdeaProjects/personal/escomic/react_frontend_ui
npm start
```

- [ ] **Step 3: Manual browser test checklist**

1. Open `http://localhost:3000`
2. In navbar dropdown, select **BM25_Wayne** — confirm it appears in list
3. Search for a book (e.g. "Batman") via search bar — confirm results load
4. Click a result book — confirm book grid loads with 20 results and facet sliders
5. Hover over books, then click another — confirm facet sliders update (personalization active)
6. Click explanation icon on a result — confirm local explanation loads (not random)
7. Select 2 books for comparison — confirm compare panel shows real explanations
8. Type free-text "batman detective crime" — confirm BM25 text results load
9. Navigate to About Us — confirm BM25_Wayne row appears in table

---

## Phase 2 Notes (Future Work)

The current BM25 corpus in `bm25_search.py::build_book_text()` weights title 3× and genre 2×, which can bias results toward genre/title matches. Planned future improvements:

1. **Reduce title/genre bias:** Change multipliers in `build_book_text()`:
   - title: `[title] * 3` → `[title]` (1× only)
   - genre: `[genre_clean] * 2` → `[genre_clean]` (1× only)

2. **Add OCR text:** Group per-panel OCR from `python_backend_api/data/metadata/COMICS_ocr_file.csv` (254 MB) by book using `groupby()` and append to `build_book_text()`. Requires user to provide grouping logic since panel-level data needs a book-id grouping key.

These changes only affect `bm25_search.py` and benefit both BM25 and BM25_Wayne systems.