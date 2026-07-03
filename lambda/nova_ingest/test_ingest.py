from .processor import process_document

with open(
    "local-api/sample_docs/fintech.txt",
    encoding="utf-8"
) as f:

    text = f.read()

chunks = process_document(
    "fintech",
    text
)

print(chunks)