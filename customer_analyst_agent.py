from crewai import Agent
from llm_config import get_llm
from research_tools import get_web_search_tool


def create_customer_analyst():
    return Agent(
        role="Market and Customer Analyst",
        goal=(
            "Analyze customer segments, customer needs, pain points, behaviors, unmet needs, "
            "purchase or adoption drivers, and relevant market demand signals."
        ),
        backstory=(
            "You are a customer strategy consultant specializing in segmentation and customer "
            "insight. You use current public evidence where available and clearly label assumptions "
            "when customer-level data is unavailable."
        ),
        tools=[get_web_search_tool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
