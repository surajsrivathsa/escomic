import os
import sys
import re
import json
import pickle
import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import common_functions.backend_utils as utils


# ──────────────────────────────────────────────────────────────
# Text building helpers
# ──────────────────────────────────────────────────────────────

_STOPWORDS = {
    "the", "a", "an", "is", "in", "of", "and", "to", "was", "it",
    "that", "he", "she", "they", "this", "with", "for", "on", "at",
    "by", "from", "or", "be", "are", "as", "has", "had", "have",
    "not", "but", "we", "you", "do", "did", "his", "her", "their",
}


def tokenize(text: str) -> list:
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    return [t for t in tokens if t not in _STOPWORDS]


def build_book_text(
    book_idx: int,
    metadata_df,
    characters_dict: dict,
    cover_dict: dict,
    w5h1_dict: dict,
) -> str:
    parts = []

    # Book title repeated 3x — high signal
    row = metadata_df.iloc[book_idx]
    title = str(row.get("Book Title", "") or "")
    if title and title != "nan":
        parts += [title] * 3

    # Genre repeated 2x — clean structured signal
    genre = str(row.get("genre", "") or "")
    if genre and genre != "nan":
        genre_clean = genre.replace("|", " ")
        parts += [genre_clean] * 2

    # Characters from character_explanations.json repeated 2x
    comic_no = int(row.get("comic_no", book_idx))
    char_info = characters_dict.get(book_idx, {})
    male_chars = char_info.get("male_characters", [])
    female_chars = char_info.get("female_characters", [])
    all_chars = [str(c) for c in (male_chars + female_chars) if c]
    if all_chars:
        parts += [" ".join(all_chars)] * 2

    # Cover keywords from comic_book_cover_prompt_dict — filtered
    cover_prompts = cover_dict.get(book_idx, [])
    filtered_prompts = [p for p in cover_prompts if utils.filter_fnc(str(p))]
    if filtered_prompts:
        parts.append(" ".join(filtered_prompts[:5]))  # cap at 5 prompts

    # W5H1 dialogue keywords (Who/What/When/Where/Why/How)
    w5h1_entry = w5h1_dict.get(comic_no, {})
    w5h1_parts = []
    for key in ("Who", "What", "When", "Where", "Why", "How"):
        val = w5h1_entry.get(key, [])
        if isinstance(val, list):
            w5h1_parts.extend(str(v) for v in val if v)
        elif val:
            w5h1_parts.append(str(val))
    if w5h1_parts:
        parts.append(" ".join(w5h1_parts))

    return " ".join(parts)


# ──────────────────────────────────────────────────────────────
# BM25 retrieval class
# ──────────────────────────────────────────────────────────────

class BM25Baseline:
    """
    Query-by-example BM25.

    Two retrieval modes:
    - retrieve(query_book_idx): pseudo-query from top TF-IDF terms of the query book
    - retrieve_by_text(query_text): tokenize raw text directly as the query
    """

    def __init__(self, metadata_df, characters_dict, cover_dict, w5h1_dict, top_k_terms=30):
        self.metadata_df = metadata_df
        self.top_k_terms = top_k_terms
        n_docs = len(metadata_df)

        print(f"[BM25] Building corpus for {n_docs} books...")
        raw_texts = [
            build_book_text(i, metadata_df, characters_dict, cover_dict, w5h1_dict)
            for i in range(n_docs)
        ]

        # BM25 index on tokenized docs
        self.tokenized_docs = [tokenize(t) for t in raw_texts]
        self.bm25 = BM25Okapi(self.tokenized_docs)

        # TF-IDF for pseudo-query extraction (QBE path only)
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
        self.tfidf_matrix = self.tfidf.fit_transform(raw_texts)
        self.feature_names = self.tfidf.get_feature_names_out()

        print(f"[BM25] Index ready. Vocab size: {len(self.feature_names)}")

    def get_pseudo_query(self, query_book_idx: int) -> list:
        """Top-K most distinctive terms from the query book via TF-IDF."""
        vec = self.tfidf_matrix[query_book_idx].toarray().flatten()
        top_indices = vec.argsort()[::-1][: self.top_k_terms]
        return [self.feature_names[i] for i in top_indices if vec[i] > 0]

    def retrieve(self, query_book_idx: int, top_n: int = 200) -> list:
        """
        QBE path: extract pseudo-query from query book → BM25 ranking.
        Returns list of dicts with our_idx and bm25_score, excludes query book.
        """
        pseudo_query = self.get_pseudo_query(query_book_idx)
        if not pseudo_query:
            return []

        scores = self.bm25.get_scores(pseudo_query).copy()
        scores[query_book_idx] = -np.inf  # exclude self

        top_indices = np.argsort(scores)[::-1][:top_n]
        return [
            {"our_idx": int(i), "bm25_score": float(scores[i])}
            for i in top_indices
            if scores[i] > -np.inf
        ]

    def retrieve_by_text(self, query_text: str, top_n: int = 200) -> list:
        """
        Free-text path: tokenize query string directly → BM25 ranking.
        Returns same format as retrieve(). No book to exclude.
        """
        tokens = tokenize(query_text)
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)
        top_indices = np.argsort(scores)[::-1][:top_n]
        return [
            {"our_idx": int(i), "bm25_score": float(scores[i])}
            for i in top_indices
        ]


# ──────────────────────────────────────────────────────────────
# Module-level singleton — built once at import time
# ──────────────────────────────────────────────────────────────

def _build_engine():
    metadata_df, _ = utils.load_book_metadata()
    # load_book_metadata returns (dict, df) — we need the raw df with Book Title column
    import common_constants.backend_constants as cst
    import pandas as pd
    raw_metadata_df = pd.read_csv(cst.BOOK_METADATA_FILEPATH)

    characters_dict = utils.load_local_explanation_characters()
    cover_dict = utils.load_local_explanation_book_cover()
    w5h1_dict = utils.load_local_explanation_w5_h1_facets()
    return BM25Baseline(raw_metadata_df, characters_dict, cover_dict, w5h1_dict)


bm25_engine = _build_engine()
