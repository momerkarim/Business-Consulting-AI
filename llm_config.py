import os
from crewai import LLM

MODEL_NAME = "openai/gpt-oss-120b"


def get_llm():
    """Create the shared Groq LLM configuration."""
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.2,
        reasoning_effort="medium",
    )
