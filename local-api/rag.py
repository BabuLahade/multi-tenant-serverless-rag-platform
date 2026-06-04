from google import genai
from dotenv import load_dotenv
import os

from retrieve import search, add_document

load_dotenv("../.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

CHAT_MODEL = "gemini-2.5-flash"


def ask(question):

    chunks = search(question)

    if not chunks:
        return {
            "answer": "I don't know.",
            "grounded": False,
            "sources": []
        }

    context = "\n\n".join(
        [chunk["text"] for chunk in chunks]
    )

    prompt = f"""
You are a support assistant.

Answer ONLY using the supplied context.

If the answer is not present in the context,
say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt
    )

    return {
        "answer": response.text,
        "grounded": True,
        "sources": ["fintech.txt"]
    }


if __name__ == "__main__":

    add_document("sample_docs/fintech.txt")

    questions = [
        "What documents are needed for KYC?",
        "What is the minimum income for a credit card?",
        "What are the loan interest rates?"
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print("QUESTION:", q)

        result = ask(q)

        print("\nANSWER:")
        print(result["answer"])