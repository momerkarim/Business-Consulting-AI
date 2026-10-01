import os

import litellm
from crewai import LLM

MODEL_NAME = "openai/gpt-oss-120b"


# ---------------------------------------------------------------------------
# Workaround for CrewAI 1.15.x + Groq:
# CrewAI tags messages with an internal "cache_breakpoint" key (used for prompt
# caching). When routed through LiteLLM, that key is sent to Groq, which rejects
# it. We strip it from every message just before the LiteLLM call.
# Remove this block once a CrewAI release with the upstream fix is installed.
# ---------------------------------------------------------------------------
def _strip_cache_breakpoint(messages):
    if not messages:
        return messages
    return [
        {k: v for k, v in m.items() if k != "cache_breakpoint"}
        if isinstance(m, dict)
        else m
        for m in messages
    ]


def _apply_litellm_patch():
    # Guard so Streamlit script reruns don't wrap the functions repeatedly.
    if getattr(litellm, "_cache_breakpoint_patched", False):
        return

    original_completion = litellm.completion

    def patched_completion(*args, **kwargs):
        if "messages" in kwargs:
            kwargs["messages"] = _strip_cache_breakpoint(kwargs["messages"])
        return original_completion(*args, **kwargs)

    litellm.completion = patched_completion

    original_acompletion = getattr(litellm, "acompletion", None)
    if original_acompletion is not None:

        async def patched_acompletion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip_cache_breakpoint(kwargs["messages"])
            return await original_acompletion(*args, **kwargs)

        litellm.acompletion = patched_acompletion

    litellm._cache_breakpoint_patched = True


_apply_litellm_patch()


def get_llm():
    """Create the shared Groq LLM configuration."""
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.2,
        reasoning_effort="medium",
    )
