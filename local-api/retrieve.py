
import numpy as np

from chunker import chunk_file
from embed import embed_text, embed_query
from repositories.vector_repository import save_chunk


vector_store = {}


def add_document(client_id, filepath):

    chunks = chunk_file(filepath)

    vector_store[client_id] = []

    print(f"Embedding {client_id}...")

    for i, chunk in enumerate(chunks):

        vector = embed_text(chunk)

        # Save to DynamoDB
        save_chunk(
            client_id,
            f"chunk_{i}",
            chunk,
            vector
        )

        # Keep local memory for now
        vector_store[client_id].append({
            "text": chunk,
            "vector": vector
        })

    print(
        f"Stored {len(chunks)} chunks for {client_id}"
    )


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search(client_id, query, top_k=5):

    if client_id not in vector_store:
        return []

    query_vector = embed_query(query)

    results = []

    for item in vector_store[client_id]:

        score = cosine_similarity(
            query_vector,
            item["vector"]
        )

        results.append({
            "text": item["text"],
            "score": float(score)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]