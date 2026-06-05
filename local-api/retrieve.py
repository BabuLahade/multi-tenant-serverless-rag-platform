# import numpy as np

# from chunker import chunk_file
# from embed import embed_text, embed_query

# # In-memory vector store
# vector_store = []


# def add_document(filepath):
#     chunks = chunk_file(filepath)

#     print(f"Embedding {len(chunks)} chunks...")

#     for i, chunk in enumerate(chunks):
#         vector = embed_text(chunk)

#         vector_store.append({
#             "text": chunk,
#             "vector": vector
#         })

#         print(f"Chunk {i+1}/{len(chunks)} embedded")

#     print(f"\nVector store size: {len(vector_store)}")


# def cosine_similarity(a, b):
#     a = np.array(a)
#     b = np.array(b)

#     return np.dot(a, b) / (
#         np.linalg.norm(a) * np.linalg.norm(b)
#     )


# def search(query, top_k=5):

#     query_vector = embed_query(query)

#     results = []

#     for item in vector_store:

#         score = cosine_similarity(
#             query_vector,
#             item["vector"]
#         )

#         results.append({
#             "text": item["text"],
#             "score": float(score)
#         })

#     results.sort(
#         key=lambda x: x["score"],
#         reverse=True
#     )

#     return results[:top_k]


# if __name__ == "__main__":

#     add_document("sample_docs/fintech.txt")

#     query = "What documents are needed for KYC?"

#     results = search(query)

#     print("\nQuery:", query)

#     print("\nTop Results:\n")

#     for i, result in enumerate(results):

#         print(f"Rank {i+1}")
#         print(f"Score: {result['score']:.4f}")

#         print(result["text"][:300])

#         print("-" * 50)
import numpy as np

from chunker import chunk_file
from embed import embed_text, embed_query


vector_store = {}


def add_document(client_id, filepath):

    chunks = chunk_file(filepath)

    vector_store[client_id] = []

    print(f"Embedding {client_id}...")

    for chunk in chunks:

        vector = embed_text(chunk)

        vector_store[client_id].append({
            "text": chunk,
            "vector": vector
        })


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