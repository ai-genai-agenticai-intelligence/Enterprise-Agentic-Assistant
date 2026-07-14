"""LLM client helpers for the direct Groq integration."""
from langchain_groq import ChatGroq

from app.config import settings


def get_langchain_llm(feature: str = "rag") -> ChatGroq:
    """Return the Groq chat model used by a LangGraph node."""
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is required to run the RAG agent.")

    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=0,
    )
