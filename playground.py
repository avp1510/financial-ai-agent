import os
from dotenv import load_dotenv
import phi.api
load_dotenv()

# Import the OOP Financial Agent System
from financial_agent_oop import FinancialAgentSystem
from phi.playground import Playground, serve_playground_app


phi.api = os.getenv("PHI_API_KEY")

# ---- CREATE FINANCIAL AGENT SYSTEM USING FACTORY PATTERN ----
# Instead of creating agents directly, we use the Factory Pattern
financial_system = FinancialAgentSystem()

# Get agents from the system using the factory pattern
finance_agent = financial_system.get_agent('finance')
websearch_agent = financial_system.get_agent('web')

# Display available agents for debugging
print("🤖 Agents created using Factory Pattern:")
print(f"  • Finance Agent: {finance_agent}")
print(f"  • Web Search Agent: {websearch_agent}")
print(f"  • Available agents: {financial_system.get_available_agents()}")

# Create playground with agents from the factory system
app = Playground(agents=[finance_agent, websearch_agent]).get_app()

if __name__ == "__main__":
    print("🚀 Starting Financial Agent Playground with OOP Factory Pattern...")
    serve_playground_app("playground:app", reload=True)