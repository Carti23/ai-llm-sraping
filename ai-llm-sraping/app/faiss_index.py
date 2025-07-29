import os

import faiss
import numpy as np

INDEX_FILE = "comment_index.faiss"

def load_faiss_index(dimension: int) -> faiss.IndexIDMap:
    if os.path.exists(INDEX_FILE):
        return faiss.read_index(INDEX_FILE)
    else:
        return faiss.IndexIDMap(faiss.IndexFlatL2(dimension))

def add_vectors_to_faiss(vectors: np.ndarray, product_id: int):
    index = load_faiss_index(vectors.shape[1])
    ids = np.array([product_id] * len(vectors), dtype='int64')
    index.add_with_ids(vectors, ids)
    save_faiss_index(index)

def save_faiss_index(index):
    faiss.write_index(index, INDEX_FILE)
