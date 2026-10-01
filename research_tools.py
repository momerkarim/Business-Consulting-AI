import os
from crewai_tools import SerperDevTool


def get_web_search_tool():
    """Return the CrewAI Serper web-search tool."""
    if not os.environ.get("SERPER_API_KEY"):
        raise RuntimeError("SERPER_API_KEY is not configured.")

    return SerperDevTool()
