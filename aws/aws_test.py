# import boto3

# sts = boto3.client("sts")

# response = sts.get_caller_identity()

# print(response)


from vector_repository import get_chunks

chunks = get_chunks("fintech")

print(f"Found {len(chunks)} chunks")

for chunk in chunks:

    print("-" * 50)

    print(chunk["chunk_id"])

    print(chunk["text"][:200])