# AI Business Consulting Team

A cloud-deployed multi-agent business consulting application built with:

- Streamlit
- CrewAI
- Groq GPT-OSS 120B
- Serper web search
- GitHub
- Streamlit Community Cloud

## Architecture

All Python files are intentionally stored in the GitHub repository root (main branch). No subfolders are required.

### Agents

1. Engagement Manager
2. Industry Research Analyst
3. Market and Customer Analyst
4. Competitive Intelligence Analyst
5. Business and Financial Analyst
6. Strategy Consultant
7. Consulting Partner / Report Writer

### Files

- `app.py` — Streamlit user interface
- `crew.py` — CrewAI orchestration
- `tasks.py` — seven consulting tasks
- `llm_config.py` — centralized Groq LLM configuration
- `research_tools.py` — Serper search configuration
- `engagement_agent.py` — Agent 1
- `industry_research_agent.py` — Agent 2
- `customer_analyst_agent.py` — Agent 3
- `competitor_analyst_agent.py` — Agent 4
- `financial_analyst_agent.py` — Agent 5
- `strategy_consultant_agent.py` — Agent 6
- `report_writer_agent.py` — Agent 7
- `requirements.txt` — Python dependencies

## Required secrets

In Streamlit Community Cloud → App settings → Secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
SERPER_API_KEY = "your_serper_api_key"
```

Never commit API keys to GitHub.

## Deployment

1. Create a GitHub repository.
2. Upload all files from this project directly to the repository's `main` branch.
3. In Streamlit Community Cloud, create a new app.
4. Select the GitHub repository.
5. Select the `main` branch.
6. Set the main file to `app.py`.
7. Add the two secrets.
8. Deploy.

## Important

The application performs web research, but research quality depends on search results and source availability. Always review important claims and sources before using the report for a real business decision.
