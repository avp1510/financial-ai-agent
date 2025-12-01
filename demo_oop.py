#!/usr/bin/env python3
"""
Demonstration of the OOP-refactored Financial Agent System
This shows the Factory Pattern implementation without requiring external dependencies
"""

from abc import ABC, abstractmethod
from typing import List, Optional


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

    def __str__(self):
        return f"AgentConfig(name='{self.name}', role='{self.role}', instructions={len(self.instructions)} items)"


# ===============================
# ABSTRACT FACTORY PATTERN
# ===============================

class AgentFactory(ABC):
    """Abstract Factory for creating different types of agents"""

    @abstractmethod
    def create_agent(self):
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

    def create_agent(self):
        config = self.get_config()
        return f"WebSearchAgent({config.name})"  # Mock agent for demo


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

    def create_agent(self):
        config = self.get_config()
        return f"FinanceAgent({config.name})"  # Mock agent for demo


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

    def create_agent(self):
        config = self.get_config()
        web_agent = self.web_factory.create_agent()
        finance_agent = self.finance_factory.create_agent()
        return f"MultiAgent({config.name}, team=[{web_agent}, {finance_agent}])"  # Mock agent for demo


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

    def get_agent(self, agent_type: str):
        """Get an agent by type"""
        return self.agents.get(agent_type.lower())

    def run_query(self, query: str, agent_type: str = 'multi', stream: bool = True):
        """Run a query using specified agent type"""
        agent = self.get_agent(agent_type)
        if not agent:
            raise ValueError(f"Unknown agent type: {agent_type}")

        if stream:
            print(f"🎯 Running query: '{query}' with {agent}")
            print("📊 Processing with multi-agent system...")
            print("✅ Query completed successfully!")
        else:
            return f"Result from {agent}: {query}"

    def get_available_agents(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.agents.keys())

    def show_system_info(self):
        """Display system information and design pattern usage"""
        print("🏗️  FINANCIAL AGENT SYSTEM - OOP REFACTORING")
        print("=" * 50)
        print("🎨 Design Pattern: ABSTRACT FACTORY PATTERN")
        print("📦 OOP Concepts Used:")
        print("  • Abstract Base Classes (ABC)")
        print("  • Inheritance (Concrete Factory Classes)")
        print("  • Encapsulation (AgentConfig class)")
        print("  • Polymorphism (Different agent creation methods)")
        print("  • Composition (MultiAgentFactory uses other factories)")
        print()
        print("🏭 Available Factories:")
        print(f"  • {self.web_factory.__class__.__name__}")
        print(f"  • {self.finance_factory.__class__.__name__}")
        print(f"  • {self.multi_factory.__class__.__name__}")
        print()
        print("🤖 Created Agents:")
        for agent_type, agent in self.agents.items():
            print(f"  • {agent_type.upper()}: {agent}")
        print()


# ===============================
# DEMONSTRATION
# ===============================

def main():
    """Demonstrate the OOP-based financial agent system"""
    print("🚀 Starting Financial Agent System Demo...")
    print()

    # Create the financial agent system
    system = FinancialAgentSystem()

    # Show system information
    system.show_system_info()

    # Demonstrate factory pattern usage
    print("🏭 FACTORY PATTERN DEMONSTRATION:")
    print("-" * 40)

    # Direct factory usage
    web_config = system.web_factory.get_config()
    finance_config = system.finance_factory.get_config()
    multi_config = system.multi_factory.get_config()

    print(f"Web Agent Config: {web_config}")
    print(f"Finance Agent Config: {finance_config}")
    print(f"Multi Agent Config: {multi_config}")
    print()

    # Demonstrate agent selection and usage
    print("🎯 AGENT USAGE DEMONSTRATION:")
    print("-" * 35)

    # Show available agents
    print(f"Available agents: {system.get_available_agents()}")
    print()

    # Run sample queries
    system.run_query("Summarize analyst recommendations for NVDA", agent_type='finance')
    print()
    system.run_query("Latest market news", agent_type='web')
    print()
    system.run_query("Comprehensive NVDA analysis with news", agent_type='multi')
    print()

    print("✅ OOP Refactoring Complete!")
    print("🎉 Benefits Achieved:")
    print("  • Better code organization and maintainability")
    print("  • Extensible factory-based agent creation")
    print("  • Clear separation of concerns")
    print("  • Type safety with abstract base classes")
    print("  • Easy to add new agent types in the future")


if __name__ == "__main__":
    main()
