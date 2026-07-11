from google import genai

from .secret_manager import get_secret


EMBED_MODEL = "gemini-embedding-2"


def get_client():

    api_key = get_secret(
        "nova/gemini_api_key"
    )

    return genai.Client(
        api_key=api_key
    )


def embed_text(text):

    client = get_client()

    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def embed_query(text):

    return embed_text(text)