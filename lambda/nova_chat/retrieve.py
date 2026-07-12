import numpy as np

# from shared.embed import embed_query
# from shared.vector_repository import get_chunks

try:
    # Running inside Lambda
    from shared.embed import embed_query
    from shared.vector_repository import get_chunks
except ImportError:
    # Running locally
    from ..shared.embed import embed_query
    from ..shared.vector_repository import get_chunks
def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )

def search(client_id, query, top_k=3):

    query_vector = embed_query(query)

    chunks = get_chunks(client_id)

    print("\n===== DEBUG =====")
    print(chunks)
    print("=================\n")

    results = []

    for chunk in chunks:

        print(chunk.keys())

        if "embedding" not in chunk:
            print("Missing embedding:", chunk)
            continue

        embedding = [
            float(x)
            for x in chunk["embedding"]
        ]

        score = cosine_similarity(
            query_vector,
            embedding
        )

        results.append({
            "text": chunk["text"],
            "score": float(score)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]