import os
from typing import Optional


def get_llm(*, temperature: float, max_tokens: int = 8000, timeout: int = 120):
    """
    Return a configured LLM instance based on available credentials.

    Priority:
    1) Gemini API key (GEMINI_API_KEY or GOOGLE_API_KEY)
    2) Vertex AI project (GOOGLE_CLOUD_PROJECT)
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project:
        from langchain_google_vertexai import ChatVertexAI

        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        return ChatVertexAI(
            model="gemini-2.5-flash",
            project=project,
            location=location,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    return None
