import os
from dotenv import load_dotenv

load_dotenv()
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# 🚨 DO NOT IMPORT OR SET openai — remove these lines!
# import openai
# openai.api_key = ...

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
 
# ---- MULTI-AGENT SUPERVISOR ----
multi_ai_agent = Agent(
    team=[websearch_agent, finance_agent],
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tool_model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    instructions=[
        "Always include sources",
        "After gathering all data from the two tools, you must stop using all tools and provide a final, complete, and combined summary in one response.",
    ],
    tools=[
        DuckDuckGo(),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True
        )
    ],
    show_tool_calls=True,
    markdown=True,
    use_tools=True,
)




multi_ai_agent.print_response(
    "Summarize analyst recommendations and share the latest news for NVDA",
    stream=True
)
# result = multi_ai_agent.run("Summarize analyst recommendations and share the latest news for NVDA")
# print(result)

# finance_agent.print_response("Get analyst recommendations for NVDA", stream=True)
# websearch_agent.print_response("Latest NVDA news", stream=True)

