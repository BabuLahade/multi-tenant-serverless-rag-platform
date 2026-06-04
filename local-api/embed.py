from google import genai
from dotenv import load_dotenv
import os

load_dotenv("../.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

EMBED_MODEL = "gemini-embedding-001"


def embed_text(text: str):
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def embed_query(query: str):
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=query
    )

    return response.embeddings[0].values


if __name__ == "__main__":
    sample_text = """
    Personal loan interest rates start from 10.5% per year.
    """

    vector = embed_text(sample_text)

    print(f"Vector length: {len(vector)}")
    print("\nFirst 10 values:")
    print(vector[:10])