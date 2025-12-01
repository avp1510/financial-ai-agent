# Financial AI Agent

A powerful multi-agent AI system that combines financial data analysis with web search capabilities to provide comprehensive market intelligence and investment insights. **Features both procedural and OOP implementations** using the Abstract Factory Pattern for enterprise-grade architecture.

## 🚀 Features

- **Real-time Stock Data**: Get current stock prices, fundamentals, and analyst recommendations
- **Company News**: Access latest news and press releases for companies
- **Web Search Integration**: Combine financial data with broader web search results
- **Multi-Agent Architecture**: Specialized agents for different types of financial queries
- **Abstract Factory Pattern**: Enterprise-grade OOP design with extensible agent creation
- **Interactive Playground**: Web-based interface using Factory Pattern
- **Streaming Responses**: Real-time response streaming for better user experience
- **Dual Implementation**: Both procedural and OOP approaches for learning

## 📊 Capabilities

### Financial Data Agent
- Stock price lookups
- Analyst recommendations with tabular display
- Company fundamentals (market cap, P/E ratio, etc.)
- Recent company news and press releases

### Web Search Agent
- General web search for financial context
- Latest market news and trends
- Economic indicators and analysis

### Multi-Agent Supervisor
- Combines both agents for comprehensive analysis
- Provides consolidated summaries from multiple data sources
- Always includes sources for transparency

## 🏗️ Architecture & Design Patterns

This project demonstrates **professional software engineering** with multiple implementation approaches:

### OOP Implementation (Abstract Factory Pattern)
- **AgentFactory**: Abstract base class for agent creation
- **WebSearchAgentFactory**: Concrete factory for web search agents
- **FinanceAgentFactory**: Concrete factory for financial data agents
- **MultiAgentFactory**: Composite factory for multi-agent systems
- **FinancialAgentSystem**: Main orchestrator using dependency injection

### Benefits of Factory Pattern
- **Extensibility**: Easy to add new agent types
- **Maintainability**: Centralized agent configuration
- **Testability**: Mock agents for unit testing
- **SOLID Principles**: Single responsibility, Open/closed, etc.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/avp1510/financial-ai-agent.git
cd financial-ai-agent
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```env
PHI_API_KEY=your_phi_api_key
GROQ_API_KEY=your_groq_api_key
```

## 🚀 Usage

### Command Line Interface

**Procedural Approach:**
```bash
python financial_agent.py
```

**OOP Approach:**
```bash
python financial_agent_oop.py
```

### Interactive Playground (OOP with Factory Pattern)

Launch the web interface:
```bash
python playground.py
```

This starts a local web server using the Factory Pattern for agent creation.

### Educational Demo

Learn about the Factory Pattern:
```bash
python demo_oop.py
```

## 💡 Example Queries

- "Summarize analyst recommendations and share the latest news for NVDA"
- "Compare Tesla and NVIDIA analyst recommendations"
- "Get current stock price for AAPL"
- "What are the fundamentals for Microsoft?"

## 📁 Project Structure

```
financial_agent/
├── 📄 README.md                    # Project documentation
├── 📋 requirements.txt             # Python dependencies
├── 🔐 .env                        # Environment variables (create this)
├── 🚫 .gitignore                  # Git exclusion rules
│
├── 🔧 Core Implementation
│   ├── financial_agent.py         # Original procedural implementation
│   └── financial_agent_oop.py     # OOP refactoring with Factory Pattern
│
├── 🌐 Web Interface
│   └── playground.py              # Web playground using Factory Pattern
│
├── 📚 Educational Content
│   ├── demo_oop.py                # Factory Pattern demonstration
│   └── chat_example.txt           # Example conversations
│
└── 🏠 Environment
    ├── venv/                      # Virtual environment
    └── myenv/                     # Alternative virtual environment
```

## 🏗️ Architecture

### Implementation Approaches

#### 1. Procedural Implementation (`financial_agent.py`)
- Direct agent instantiation
- Global variable usage
- Simple but less maintainable
- Good for quick prototyping

#### 2. OOP Implementation (`financial_agent_oop.py`)
- Abstract Factory Pattern
- Clean separation of concerns
- Extensible and maintainable
- Enterprise-grade architecture

### Agent Types

1. **Finance Agent**: Specialized in financial data retrieval using YFinance tools
   - Stock prices and fundamentals
   - Analyst recommendations
   - Company news

2. **Web Search Agent**: Handles general web searches using DuckDuckGo
   - Market news and trends
   - Economic data
   - General financial information

3. **Multi-Agent Supervisor**: Orchestrates both agents for complex queries
   - Combines data from multiple sources
   - Provides unified responses
   - Ensures source attribution

### Technology Stack

- **Phi Framework**: Multi-agent orchestration
- **Groq**: Llama 4 Scout model for AI processing
- **YFinance**: Financial data retrieval
- **DuckDuckGo**: Web search capabilities
- **FastAPI**: Web playground backend
- **Uvicorn**: ASGI web server
- **Python ABC**: Abstract base classes for OOP

### Design Patterns Demonstrated

- **Abstract Factory Pattern**: For extensible agent creation
- **Strategy Pattern**: Different agents as different strategies
- **Facade Pattern**: Multi-agent supervisor as unified interface
- **Composite Pattern**: Multi-agent system composition
- **Template Method**: Consistent agent configuration structure

## 🔧 Configuration

The agents are configured with the following models and tools:

- **Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Financial Tools**: YFinance (price, fundamentals, recommendations, news)
- **Search Tools**: DuckDuckGo web search
- **Factory Pattern**: Extensible agent creation system

## 📝 Dependencies

Key dependencies include:
- `phidata`: Multi-agent framework
- `groq`: AI model provider
- `yfinance`: Financial data
- `ddgs`: DuckDuckGo search
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `python-dotenv`: Environment variable management

## 🎯 Running Different Versions

### Quick Start (Recommended)
```bash
# Clone and setup
git clone https://github.com/avp1510/financial-ai-agent.git
cd financial-ai-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Create .env file with your API keys
echo "PHI_API_KEY=your_key_here" > .env
echo "GROQ_API_KEY=your_key_here" >> .env

# Run the web playground (Factory Pattern)
python playground.py
```

### Compare Implementations
```bash
# Procedural approach (simple)
python financial_agent.py

# OOP approach (advanced architecture)
python financial_agent_oop.py

# Learn design patterns (no API keys needed)
python demo_oop.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test both procedural and OOP implementations
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Learning Outcomes

This project demonstrates:
- **Multi-agent AI systems** with specialized agents
- **Abstract Factory Pattern** for extensible design
- **OOP principles** (encapsulation, inheritance, polymorphism)
- **Clean architecture** and SOLID principles
- **Web development** with FastAPI
- **Financial data APIs** integration
- **Professional code organization**

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Not financial advice. Always do your own research and consult with financial professionals before making investment decisions.

## 🔍 Example Output

The agent provides structured responses including:

- Tabular analyst recommendations
- Summarized news headlines
- Source attribution
- Combined analysis from multiple data sources

See `chat_example.txt` for detailed example interactions.

## 🏆 Key Achievements

- ✅ **Dual Implementation**: Both procedural and OOP approaches
- ✅ **Design Patterns**: Abstract Factory, Strategy, Facade patterns
- ✅ **Enterprise Architecture**: Extensible and maintainable code
- ✅ **Web Deployment**: Interactive playground interface
- ✅ **Professional Documentation**: Comprehensive README and examples
- ✅ **Version Control**: Git with proper .gitignore
- ✅ **Environment Management**: Virtual environments and dependency management
