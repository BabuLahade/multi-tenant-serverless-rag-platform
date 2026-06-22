
from vector_repository import get_chunks

chunks = get_chunks("fintech")

print(f"Found {len(chunks)} chunks")

for chunk in chunks:

    print("-" * 50)

    print(chunk["chunk_id"])

    print(chunk["text"][:200])
    
    
# from vector_repository import get_chunks

# chunks = get_chunks("fintech")

# print(f"Found {len(chunks)} chunks")

# for chunk in chunks:

#     print("-" * 50)

#     print(chunk["chunk_id"])

#     print(chunk["text"][:200])
