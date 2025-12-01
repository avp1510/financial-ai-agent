import os
from dotenv import load_dotenv
import phi.api 
load_dotenv()
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app


phi.api = os.getenv("PHI_API_KEY")

# ---- WEB SEARCH AGENT ----
websearch_agent = Agent(
    name="Web search Agent",
    role="Search web for the information",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    use_tools=True,
    markdown=True
)

# ---- FINANCIAL DATA AGENT ----
finance_agent = Agent(
    name="Finance AI Agent",
    # role="Fetch financial data and answer questions based on it.",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True
        )
    ],
    use_tools=True,
    instructions=[
        "Use tables to display analyst recommendations",
        "Only return analyst recommendations when asked",
        "Do not include analyst recommendations when asked for company news"
    ],
    show_tool_calls=True,
    markdown=True
)
 
app = Playground(agents=[finance_agent, websearch_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)