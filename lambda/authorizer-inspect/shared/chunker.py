def chunk_text(text, chunk_size=500, overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def chunk_file(filepath):

    with open(filepath, "r", encoding="utf-8") as f:

        text = f.read()

    return chunk_text(text)