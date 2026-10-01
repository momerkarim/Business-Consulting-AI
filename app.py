import os
import streamlit as st

st.set_page_config(
    page_title="AI Business Consulting Team",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Business Consulting Team")
st.caption("Research • Analysis • Strategy • Executive Report")

# Streamlit Cloud stores secrets in st.secrets.
# We copy them to environment variables because CrewAI/LiteLLM reads
# GROQ_API_KEY and SERPER_API_KEY from the environment.
for key in ("GROQ_API_KEY", "SERPER_API_KEY"):
    if key in st.secrets:
        os.environ[key] = st.secrets[key]

with st.sidebar:
    st.header("Consulting Engagement")
    st.write("Seven specialized AI consultants will research and analyze the case.")

company = st.text_input("Company / Organization", placeholder="e.g., ABC Telecom")
industry = st.text_input("Industry", placeholder="e.g., Telecommunications")
country = st.text_input("Country / Market", placeholder="e.g., Pakistan")
challenge = st.text_area(
    "Business Challenge",
    placeholder="Describe the business problem, opportunity, or decision you want to analyze.",
    height=140,
)
objective = st.text_area(
    "Business Objective",
    placeholder="What should the consulting team help the organization achieve?",
    height=120,
)
additional_context = st.text_area(
    "Additional Context (optional)",
    placeholder="Existing products, target customers, constraints, competitors, known figures, etc.",
    height=120,
)

generate = st.button("🚀 Generate Business Strategy Report", type="primary", use_container_width=True)

if generate:
    missing = []
    if not company.strip():
        missing.append("Company / Organization")
    if not industry.strip():
        missing.append("Industry")
    if not country.strip():
        missing.append("Country / Market")
    if not challenge.strip():
        missing.append("Business Challenge")
    if not objective.strip():
        missing.append("Business Objective")

    if missing:
        st.error("Please complete: " + ", ".join(missing))
        st.stop()

    if not os.environ.get("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Add it under Streamlit Cloud → App settings → Secrets.")
        st.stop()

    if not os.environ.get("SERPER_API_KEY"):
        st.error("SERPER_API_KEY is missing. Add it under Streamlit Cloud → App settings → Secrets.")
        st.stop()

    inputs = {
        "company": company.strip(),
        "industry": industry.strip(),
        "country": country.strip(),
        "challenge": challenge.strip(),
        "objective": objective.strip(),
        "additional_context": additional_context.strip() or "No additional context provided.",
    }

    try:
        from crew import build_crew

        progress = st.status("Building the consulting team...", expanded=True)

        progress.write("1/7 — Engagement Manager")
        progress.write("2/7 — Industry Research Analyst")
        progress.write("3/7 — Market & Customer Analyst")
        progress.write("4/7 — Competitor Analyst")
        progress.write("5/7 — Business & Financial Analyst")
        progress.write("6/7 — Strategy Consultant")
        progress.write("7/7 — Partner / Report Writer")

        crew = build_crew()

        progress.update(label="Running consulting engagement...", state="running")
        result = crew.kickoff(inputs=inputs)
        progress.update(label="Consulting report completed", state="complete")

        report = getattr(result, "raw", str(result))

        st.success("Business strategy report generated.")

        st.download_button(
            label="⬇️ Download Markdown Report",
            data=report,
            file_name=f"{company.lower().replace(' ', '_')}_business_strategy.md",
            mime="text/markdown",
            use_container_width=True,
        )

        st.markdown("## Business Strategy Report")
        st.markdown(report)

    except Exception as exc:
        st.error("The consulting workflow failed.")
        st.exception(exc)
        st.info(
            "If this is a deployment error, copy the complete traceback and send it to ChatGPT. "
            "We can fix the affected file without rebuilding the whole project."
        )
