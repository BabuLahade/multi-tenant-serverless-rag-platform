 from google import genai

# from retrieve import search
# from shared.secret_manager import get_secret

try:
    # Running inside Lambda
    from retrieve import search
    from shared.secret_manager import get_secret
except ImportError:
    # Running locally
    from .retrieve import search
    from ..shared.secret_manager import get_secret
def ask(client_id, question):

    chunks = search(
        client_id,
        question
    )

    context = "\n\n".join(
        [c["text"] for c in chunks]
    )

    api_key = get_secret(
        "nova/gemini_api_key"
    )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
Answer using only provided context.

Context:

{context}

Question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": len(chunks),
        "grounded": True
    }