from lambda.shared.chunker import chunk_text
from lambda.shared.embed import embed_text
from lambda.shared.vector_repository import save_chunk


def process_document(client_id, text):

    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        embedding = embed_text(chunk)

        save_chunk(
            client_id,
            f"chunk_{i}",
            chunk,
            embedding
        )

    return len(chunks)