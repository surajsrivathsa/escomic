import os, sys
import pandas as pd, numpy as np
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import common_functions.backend_utils as utils
from search.coarse import coarse_search
from search.coarse import bm25_search

book_metadata_dict, comic_book_metadata_df = utils.load_book_metadata()
comic_book_metadata_df.rename(
    columns={"Book Title": "book_title", "Year": "year"}, inplace=True
)
comic_book_metadata_df.fillna("", inplace=True)


def perform_coarse_search(
    b_id: int,
    feature_weight_dict={
        "cld": 0.1,
        "edh": 0.1,
        "hog": 0.1,
        "text": 1.0,
        "comic_img": 1.0,
        "comic_txt": 1.0,
    },
    top_n=200,
):

    # query_book_comic_id = b_id # 1262 # 1647(tin-tin), 520(aquaman), 558(asterix), 587(Avengers), 650(Batman), 1270(Justice Society)

    top_n_results_df = coarse_search.comics_coarse_search(
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

    print("Query Book : {} ".format(b_id))
    # return (coarse_filtered_book_new_lst, coarse_filtered_book_df)
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)


def perform_coarse_search_without_reranking(
    b_id: int, feature_weight_dict: dict, top_n: int
):
    top_n_results_df = coarse_search.comics_coarse_search_without_reranking(
        query_comic_book_id=b_id, feature_weight_dict=feature_weight_dict, top_n=top_n
    )
    coarse_filtered_book_df = top_n_results_df[
        ["comic_no", "book_title", "genre", "year"]
    ]

    query_book_obj = book_metadata_dict[b_id]  # get querry object details

    coarse_filtered_book_df.fillna("", inplace=True)

    coarse_filtered_book_lst = coarse_filtered_book_df.to_dict("records")
    coarse_filtered_book_new_lst = []

    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        coarse_filtered_book_new_lst.append(d)

    print("Query Book : {} ".format(b_id))

    coarse_filtered_book_lst.insert(
        7,
        {
            "comic_no": query_book_obj[0],
            "book_title": query_book_obj[1],
            "genre": str(query_book_obj[2]),
            "year": query_book_obj[3]
            if not isinstance(query_book_obj[3], str)
            and not math.isnan(query_book_obj[3])
            else 1950,
            "query_book": True,
        },
    )

    coarse_filtered_book_new_lst = []
    print(coarse_filtered_book_lst[:2])

    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        if "query_book" not in d:
            d["query_book"] = False
        d["thumbsUp"] = 0
        d["thumbsDown"] = 0

        coarse_filtered_book_new_lst.append(d)
    # return (coarse_filtered_book_new_lst, coarse_filtered_book_df)
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)


def perform_random_search(b_id: int, feature_weight_dict: dict, top_n: int):
    top_n_results_dict = coarse_search.comics_random_search(
        query_comic_book_id=b_id, feature_weight_dict=feature_weight_dict, top_n=top_n
    )

    query_book_obj = book_metadata_dict[b_id]  # get query object details
    coarse_filtered_book_lst = []
    coarse_filtered_book_new_lst = []

    for idx, d in enumerate(top_n_results_dict):
        coarse_filtered_book_lst.append(d)

    coarse_filtered_book_lst.insert(
        7,
        {
            "comic_no": query_book_obj[0],
            "book_title": query_book_obj[1],
            "genre": str(query_book_obj[2]),
            "year": query_book_obj[3]
            if not isinstance(query_book_obj[3], str)
            and not math.isnan(query_book_obj[3])
            else 1950,
            "query_book": True,
        },
    )

    print(coarse_filtered_book_lst[:2], len(coarse_filtered_book_lst))

    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        if "query_book" not in d:
            d["query_book"] = False
        d["thumbsUp"] = 0
        d["thumbsDown"] = 0

        coarse_filtered_book_new_lst.append(d)

    coarse_filtered_book_df = pd.DataFrame.from_records(coarse_filtered_book_new_lst)
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)


def perform_bm25_search(b_id: int, top_n: int = 200):
    """BM25 query-by-example: pseudo-query from query book → BM25 ranking."""
    bm25_results = bm25_search.bm25_engine.retrieve(b_id, top_n=top_n + 1)

    query_book_obj = book_metadata_dict[b_id]
    coarse_filtered_book_lst = []

    for result in bm25_results:
        idx = result["our_idx"]
        try:
            comic_no, book_title, genre, year = book_metadata_dict[idx]
        except Exception:
            continue
        coarse_filtered_book_lst.append({
            "comic_no": comic_no,
            "book_title": book_title,
            "genre": str(genre),
            "year": year if not isinstance(year, str) and not math.isnan(year) else 1950,
            "query_book": False,
        })

    # insert query book at position 7 (same pattern as perform_coarse_search_without_reranking)
    coarse_filtered_book_lst.insert(
        7,
        {
            "comic_no": query_book_obj[0],
            "book_title": query_book_obj[1],
            "genre": str(query_book_obj[2]),
            "year": query_book_obj[3]
            if not isinstance(query_book_obj[3], str) and not math.isnan(query_book_obj[3])
            else 1950,
            "query_book": True,
        },
    )

    coarse_filtered_book_new_lst = []
    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        d.setdefault("query_book", False)
        d["thumbsUp"] = 0
        d["thumbsDown"] = 0
        coarse_filtered_book_new_lst.append(d)

    coarse_filtered_book_df = pd.DataFrame.from_records(coarse_filtered_book_new_lst)
    print(f"BM25 QBE Query Book: {b_id}")
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)


def perform_bm25_text_search(query_text: str, top_n: int = 200):
    """BM25 free-text search: tokenize raw text query → BM25 ranking."""
    bm25_results = bm25_search.bm25_engine.retrieve_by_text(query_text, top_n=top_n)

    coarse_filtered_book_lst = []
    for result in bm25_results:
        idx = result["our_idx"]
        try:
            comic_no, book_title, genre, year = book_metadata_dict[idx]
        except Exception:
            continue
        coarse_filtered_book_lst.append({
            "comic_no": comic_no,
            "book_title": book_title,
            "genre": str(genre),
            "year": year if not isinstance(year, str) and not math.isnan(year) else 1950,
            "query_book": False,
        })

    coarse_filtered_book_new_lst = []
    for idx, d in enumerate(coarse_filtered_book_lst):
        d["id"] = idx
        d["thumbsUp"] = 0
        d["thumbsDown"] = 0
        coarse_filtered_book_new_lst.append(d)

    coarse_filtered_book_df = pd.DataFrame.from_records(coarse_filtered_book_new_lst)
    print(f"BM25 Free-text Query: '{query_text}'")
    return (coarse_filtered_book_new_lst, coarse_filtered_book_df)

