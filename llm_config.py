import asyncio
import os
import re
import time

import litellm
from crewai import LLM

MODEL_NAME = "openai/gpt-oss-120b"

# Rate-limit retry settings (Groq free tier has a low tokens-per-minute cap).
MAX_RATE_LIMIT_RETRIES = 8
MAX_WAIT_SECONDS = 65
DEFAULT_WAIT_SECONDS = 20


# ---------------------------------------------------------------------------
# Workaround 1 (CrewAI 1.15.x + Groq):
# CrewAI tags messages with an internal "cache_breakpoint" key (used for prompt
# caching). When routed through LiteLLM, that key is sent to Groq, which rejects
# it. We strip it from every message just before the LiteLLM call.
# Remove this once a CrewAI release with the upstream fix is installed.
#
# Workaround 2 (Groq rate limits):
# On a RateLimitError we wait for the time Groq suggests ("try again in Xs")
# and retry, instead of failing the whole consulting workflow.
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


def _wait_time(error, attempt):
    """Parse Groq's suggested wait (e.g. '26.6s' or '1m2.5s'); fall back to backoff."""
    match = re.search(r"try again in (?:(\d+)m)?(\d+(?:\.\d+)?)s", str(error))
    if match:
        minutes = int(match.group(1) or 0)
        seconds = float(match.group(2))
        wait = minutes * 60 + seconds + 2  # small safety margin
    else:
        wait = DEFAULT_WAIT_SECONDS * (attempt + 1)
    return min(wait, MAX_WAIT_SECONDS)


def _apply_litellm_patch():
    # Guard so Streamlit script reruns don't wrap the functions repeatedly.
    if getattr(litellm, "_groq_patch_applied", False):
        return

    original_completion = litellm.completion

    def patched_completion(*args, **kwargs):
        if "messages" in kwargs:
            kwargs["messages"] = _strip_cache_breakpoint(kwargs["messages"])
        for attempt in range(MAX_RATE_LIMIT_RETRIES + 1):
            try:
                return original_completion(*args, **kwargs)
            except litellm.RateLimitError as e:
                if attempt >= MAX_RATE_LIMIT_RETRIES:
                    raise
                time.sleep(_wait_time(e, attempt))

    litellm.completion = patched_completion

    original_acompletion = getattr(litellm, "acompletion", None)
    if original_acompletion is not None:

        async def patched_acompletion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip_cache_breakpoint(kwargs["messages"])
            for attempt in range(MAX_RATE_LIMIT_RETRIES + 1):
                try:
                    return await original_acompletion(*args, **kwargs)
                except litellm.RateLimitError as e:
                    if attempt >= MAX_RATE_LIMIT_RETRIES:
                        raise
                    await asyncio.sleep(_wait_time(e, attempt))

        litellm.acompletion = patched_acompletion

    litellm._groq_patch_applied = True


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
