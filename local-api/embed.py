# embed.py
# Calls Gemini API to convert text into a vector

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv("../.env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/text-embedding-004"


def embed_text(text):
    result = genai.embed_content(
        model=MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return result["embedding"]


def embed_query(text):
    result = genai.embed_content(
        model=MODEL,
        content=text,
        task_type="retrieval_query"
    )
    return result["embedding"]


if __name__ == "__main__":
    vector = embed_text("What is the interest rate for personal loans?")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")