import os

import numpy as np
import pytest

from app.faiss_index import (
    INDEX_FILE,
    add_vectors_to_faiss,
    load_faiss_index,
    save_faiss_index,
    search_faiss,
)


def test_load_faiss_index_creates_new_index():
    dimension = 128
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
    index = load_faiss_index(dimension)
    assert index.ntotal == 0


def test_add_vectors_to_faiss():
    vectors = np.random.rand(10, 128).astype('float32')
    product_id = 1
    add_vectors_to_faiss(vectors, product_id)
    index = load_faiss_index(128)
    assert index.ntotal == 10


def test_search_faiss():
    vectors = np.random.rand(10, 128).astype('float32')
    product_id = 1
    add_vectors_to_faiss(vectors, product_id)
    query_vector = np.random.rand(1, 128).astype('float32')
    distances, ids = search_faiss(query_vector)
    assert len(distances) == 3
    assert len(ids) == 3


def test_search_faiss_no_index():
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
    query_vector = np.random.rand(1, 128).astype('float32')
    with pytest.raises(RuntimeError, match="FAISS індекс ще не створено."):
        search_faiss(query_vector) 