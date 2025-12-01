import os
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo


# ===============================
# CONFIGURATION CLASSES
# ===============================

class AgentConfig:
    """Configuration class for agent parameters"""
    def __init__(self,
                 name: str,
                 model_id: str = "meta-llama/llama-4-scout-17b-16e-instruct",
                 role: Optional[str] = None,
                 instructions: Optional[List[str]] = None,
                 show_tool_calls: bool = True,
                 use_tools: bool = True,
                 markdown: bool = True):
        self.name = name
        self.model_id = model_id
        self.role = role
        self.instructions = instructions or []
        self.show_tool_calls = show_tool_calls
        self.use_tools = use_tools
        self.markdown = markdown


# ===============================
# ABSTRACT FACTORY PATTERN
# ===============================

class AgentFactory(ABC):
    """Abstract Factory for creating different types of agents"""

    @abstractmethod
    def create_agent(self) -> Agent:
        """Create and return an agent instance"""
        pass

    @abstractmethod
    def get_config(self) -> AgentConfig:
        """Get the configuration for this agent type"""
        pass


# ===============================
# CONCRETE FACTORY CLASSES
# ===============================

class WebSearchAgentFactory(AgentFactory):
    """Factory for creating web search agents"""

    def get_config(self) -> AgentConfig:
        return AgentConfig(
            name="Web Search Agent",
            role="Search web for information",
            instructions=["Always include sources"]
        )

    def create_agent(self) -> Agent:
        config = self.get_config()
        return Agent(
            name=config.name,
            role=config.role,
            model=Groq(id=config.model_id),
            tools=[DuckDuckGo()],
            instructions=config.instructions,
            show_tool_calls=config.show_tool_calls,
            use_tools=config.use_tools,
            markdown=config.markdown
        )


class FinanceAgentFactory(AgentFactory):
    """Factory for creating financial data agents"""

    def get_config(self) -> AgentConfig:
        return AgentConfig(
            name="Finance AI Agent",
            instructions=[
                "Use tables to display analyst recommendations",
                "Only return analyst recommendations when asked",
                "Do not include analyst recommendations when asked for company news"
            ]
        )

    def create_agent(self) -> Agent:
        config = self.get_config()
        return Agent(
            name=config.name,
            model=Groq(id=config.model_id),
            tools=[YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                stock_fundamentals=True,
                company_news=True
            )],
            instructions=config.instructions,
            show_tool_calls=config.show_tool_calls,
            use_tools=config.use_tools,
            markdown=config.markdown
        )


class MultiAgentFactory(AgentFactory):
    """Factory for creating multi-agent supervisors"""

    def __init__(self, web_factory: WebSearchAgentFactory, finance_factory: FinanceAgentFactory):
        self.web_factory = web_factory
        self.finance_factory = finance_factory

    def get_config(self) -> AgentConfig:
        return AgentConfig(
            name="Multi-Agent Supervisor",
            instructions=[
                "Always include sources",
                "After gathering all data from the two tools, you must stop using all tools and provide a final, complete, and combined summary in one response."
            ]
        )

    def create_agent(self) -> Agent:
        config = self.get_config()
        web_agent = self.web_factory.create_agent()
        finance_agent = self.finance_factory.create_agent()

        return Agent(
            name=config.name,
            team=[web_agent, finance_agent],
            model=Groq(id=config.model_id),
            tool_model=Groq(id=config.model_id),
            instructions=config.instructions,
            tools=[
                DuckDuckGo(),
                YFinanceTools(
                    stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True,
                    company_news=True
                )
            ],
            show_tool_calls=config.show_tool_calls,
            markdown=config.markdown,
            use_tools=config.use_tools
        )


# ===============================
# MAIN SYSTEM ORCHESTRATOR
# ===============================

class FinancialAgentSystem:
    """Main system class that orchestrates all agents using Factory Pattern"""

    def __init__(self):
        # Initialize factories
        self.web_factory = WebSearchAgentFactory()
        self.finance_factory = FinanceAgentFactory()
        self.multi_factory = MultiAgentFactory(self.web_factory, self.finance_factory)

        # Create agents using factories
        self.web_agent = self.web_factory.create_agent()
        self.finance_agent = self.finance_factory.create_agent()
        self.multi_agent = self.multi_factory.create_agent()

        # Registry of available agents
        self.agents = {
            'web': self.web_agent,
            'finance': self.finance_agent,
            'multi': self.multi_agent
        }

    def get_agent(self, agent_type: str) -> Agent:
        """Get an agent by type"""
        return self.agents.get(agent_type.lower())

    def run_query(self, query: str, agent_type: str = 'multi', stream: bool = True):
        """Run a query using specified agent type"""
        agent = self.get_agent(agent_type)
        if not agent:
            raise ValueError(f"Unknown agent type: {agent_type}")

        if stream:
            agent.print_response(query, stream=True)
        else:
            return agent.run(query)

    def get_available_agents(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.agents.keys())


# ===============================
# USAGE EXAMPLE
# ===============================

if __name__ == "__main__":
    # Create the financial agent system
    system = FinancialAgentSystem()

    # Example usage
    print("Available agents:", system.get_available_agents())

    # Run query using multi-agent system
    system.run_query(
        "Summarize analyst recommendations and share the latest news for NVDA",
        agent_type='multi',
        stream=True
    )

    # Alternative: Use individual agents
    # system.run_query("Get analyst recommendations for NVDA", agent_type='finance')
    # system.run_query("Latest NVDA news", agent_type='web')
