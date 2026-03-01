from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# Load pretrained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embeddings(text_list):
    embeddings = model.encode(text_list)
    return np.array(embeddings)


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def save_index(index, file_path):
    faiss.write_index(index, file_path)


def load_index(file_path):
    return faiss.read_index(file_path)


def search_similar(index, query, text_list, top_k=5):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        results.append(text_list[i])

    return results