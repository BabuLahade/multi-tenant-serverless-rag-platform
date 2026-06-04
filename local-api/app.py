from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

from retrieve import add_document
from rag import ask

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading documents...")

    docs_path = "sample_docs"

    for filename in os.listdir(docs_path):

        if filename.endswith(".txt"):
            add_document(
                f"{docs_path}/{filename}"
            )

    print("Knowledge base loaded.")
    yield


app = FastAPI(
    title="Nova AI Platform",
    version="1.0",
    lifespan=lifespan
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    result = ask(request.message)

    return ChatResponse(
        answer=result["answer"],
        grounded=result["grounded"],
        sources=result["sources"]
    )