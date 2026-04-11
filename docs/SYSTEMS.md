# ESCOMIC: Search Systems Overview

ESCOMIC includes multiple search systems with different configurations, optimized for different research questions and user preferences. You can choose which system to use from the frontend interface.

## System Configurations

### 🌟 Wayne (Default - Recommended)

**Full Featured System - Has everything!**

| Feature | Status |
|---------|--------|
| Personalization | ✅ Yes |
| Reranking | ✅ Yes |
| Comparison | ✅ Yes |
| Relevance Feedback | ✅ Interactive |
| Explanations | ✅ Visual & Textual |

**Best For:**
- First-time users
- Production use
- Learning what the system can do

**Endpoints:**
- Search: `/book_search_with_searchbar_inputs`
- Comparison: `/compare_books`
- Explanations: `/local_explanation`

---

### ⚙️ Stark

**Personalization + Reranking, Random Comparison**

| Feature | Status |
|---------|--------|
| Personalization | ✅ Yes |
| Reranking | ✅ Yes |
| Comparison | ⚠️ Random (Baseline) |
| Relevance Feedback | ✅ Interactive |
| Explanations | ✅ Visual & Textual |

**Differs from Wayne:**
- Comparison results are randomized instead of based on similarity

**Best For:**
- Testing if comparison quality matters
- Baseline for Wayne

**Endpoints:**
- Search: `/book_search_with_searchbar_inputs`
- Comparison: `/compare_books_with_random`

---

### 📍 Croft

**Personalization + Reranking, Random Feedback Explanations**

| Feature | Status |
|---------|--------|
| Personalization | ✅ Yes |
| Reranking | ✅ Yes |
| Comparison | ✅ Yes |
| Relevance Feedback | ⚠️ Random (Baseline) |
| Explanations | ✅ Visual & Textual |

**Differs from Wayne:**
- Relevance feedback explanations are randomized

**Best For:**
- Testing if explanation quality affects user satisfaction
- Evaluating explanation effectiveness

**Endpoints:**
- Book Grid: `/book_search_with_random_explanation_feedback` 
- Search: `/book_search_with_searchbar_inputs`

---

### 🔩 Butcher

**No Personalization, No Reranking (Baseline)**

| Feature | Status |
|---------|--------|
| Personalization | ❌ No |
| Reranking | ❌ No |
| Comparison | ✅ Yes |
| Relevance Feedback | ✅ Interactive |
| Explanations | ✅ Visual & Textual |

**Differences from Wayne:**
- No user personalization
- No adaptive reranking
- Static results

**Best For:**
- Baseline system
- Testing impact of personalization
- Comparing against non-adaptive search

**Endpoints:**
- Book Grid: `/book_search_with_no_personalization?b_id=`
- Search: `/book_search_with_searchbar_inputs`
- Comparison: `/compare_books`

---

### 🎲 Gray

**Random Personalization, Random Reranking**

| Feature | Status |
|---------|--------|
| Personalization | 🎲 Random |
| Reranking | 🎲 Random |
| Comparison | ✅ Yes |
| Relevance Feedback | ✅ Interactive |
| Explanations | ✅ Visual & Textual |

**Differs from Wayne:**
- Personalization is randomized
- Reranking is randomized

**Best For:**
- Testing if real personalization adds value
- Measuring impact of intelligent ranking

**Endpoints:**
- Search Bar: `/book_search_with_searchbar_inputs_and_random_serp`
- Book Grid: `/book_search_with_random_serp_results?b_id=`
- Comparison: `/compare_books`

---

### 🔤 BM25 *(Added April 10, 2026)*

**Probabilistic Text Ranking — Free-Text Search Support**

> BM25 (Best Match 25) is a probabilistic ranking algorithm that scores documents based on term frequency and inverse document frequency, with length normalization.

| Feature | Status |
|---------|--------|
| Ranking Engine | ✅ BM25 (Okapi BM25) |
| Free-Text Search | ✅ Yes (type any query) |
| Query by Example | ✅ Yes (select a book) |
| Personalization | ❌ No |
| Reranking | ❌ No |
| Comparison | ✅ Yes |
| Relevance Feedback | 🎲 Random |
| Explanations | 🎲 Random |

**How it works:**
- **Query by Example (book-click):** Top TF-IDF terms from the selected book are extracted as a pseudo-query, then ranked against all books using BM25. Facet weights are assigned randomly.
- **Free-Text Search:** The typed query is tokenized and matched directly against the BM25 corpus. All facet weights default to 1.0.

**Text corpus per book:**
- Title (weighted ×3)
- Genre (weighted ×2)
- Characters (weighted ×2)
- Cover keywords (filtered)
- W5H1 dialogue keywords (Who/What/When/Where/Why/How)

**Differs from all other variants:**
- Uses BM25 probabilistic ranking instead of TF-IDF cosine similarity
- No adaptive personalization or reranking
- Supports raw free-text queries natively

**Best For:**
- Keyword-based searches (e.g., "batman detective crime gotham")
- Exploring BM25 vs TF-IDF retrieval quality
- Free-text search without needing to know a specific book title

**Endpoints:**
- Book Grid: `/book_search_with_bm25?b_id=`
- Search Bar: `/book_search_with_bm25_searchbar`
- Comparison: `/compare_books`

---

## Research Questions Addressed

### RQ1: Does Comparison Quality Matter?
- **Wayne** vs **Stark**
- Wayne has intelligent comparison, Stark uses random
- Difference: Comparison algorithm effectiveness

### RQ2: Do Explanation Quality Matter?
- **Wayne** vs **Croft**
- Wayne has intelligent feedback explanations, Croft uses random
- Difference: Explanation quality impact

### RQ3: What Features Drive Results?
- **Wayne** vs **Butcher** vs **Gray**
- Wayne: Full system
- Butcher: No personalization/reranking (baseline)
- Gray: Random personalization/reranking (control)
- Impact of personalization and intelligent reranking

---

## Switching Systems

### From Frontend UI

1. Open ESCOMIC in your browser
2. Look for system selection (usually in settings or header)
3. Choose desired system:
   - Wayne (default)
   - Stark
   - Croft
   - Butcher
   - Gray
   - BM25 *(free-text search)*
4. Your preference is saved for the session

### Via API

All systems use same API structure, switching based on selected endpoints:

```python
# Example: Using Wayne vs Butcher for comparison

# Wayne (intelligent comparison)
response = requests.post(
    "http://localhost:8000/compare_books",
    json={"book1_id": 542, "book2_id": 564}
)

# Butcher (same comparison)
response = requests.post(
    "http://localhost:8000/compare_books",  # Same endpoint
    json={"book_id": 564}
)
```

---

## Performance & Features Summary

| Feature | Wayne | Stark | Croft | Butcher | Gray | BM25 |
|---------|:-----:|:-----:|:-----:|:-------:|:----:|:----:|
| Personalization | ✅ | ✅ | ✅ | ❌ | 🎲 | ❌ |
| Reranking | ✅ | ✅ | ✅ | ❌ | 🎲 | ❌ |
| Comparison | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Feedback Explain | ✅ | ✅ | ⚠️ | ✅ | ✅ | 🎲 |
| Free-Text Search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ranking Engine | TF-IDF | TF-IDF | TF-IDF | TF-IDF | TF-IDF | **BM25** |
| System Speed | Normal | Normal | Normal | Fastest | Normal | Fast |
| Complexity | High | High | High | Low | Medium | Low |
| Recommended | **YES** | Research | Research | Research | Research | Free-Text |

> **Note (April 10, 2026):** All variants now support free-text search (powered by BM25). The BM25 variant additionally uses BM25 for query-by-example book-click searches.

---

## Recommendations

### For First-Time Users
→ Use **Wayne** to see full system capabilities

### For Production
→ Use **Wayne** for best user experience

### For Research/Evaluation
→ Try all combinations:
- Compare **Wayne** vs **Butcher** (baseline)
- Compare **Wayne** vs **Gray** (random control)
- A/B test **Wayne** vs **Stark**

### For Minimal Personalization
→ Use **Butcher** (no personalization baseline)

### For Free-Text / Keyword Search
→ Use **BM25** for raw keyword queries (e.g., "batman crime detective gotham")

---

## Technical Details

All systems use the same underlying:
- Content extraction (visual + textual features)
- Search index
- Explanation mechanisms

**They differ only in:**
- Whether personalization is applied
- Whether reranking is applied
- Whether explanations are random/intelligent

This ensures fair comparison for research evaluation.

---

## Next Steps

- Back to [README](../README.md)
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for system-specific issues
- Check [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md) for command reference
