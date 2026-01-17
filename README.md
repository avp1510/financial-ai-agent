# Financial AI Agent

A powerful multi-agent AI system that combines financial data analysis with web search capabilities to provide comprehensive market intelligence and investment insights.

## 🏗️ Architecture Excellence

**Domain Driven Design (DDD)** with **Test Driven Development (TDD)** and comprehensive **fault tolerance** patterns for enterprise-grade reliability.

- **DDD Architecture**: Clean separation of domain logic, application services, and infrastructure
- **TDD Implementation**: 48 comprehensive tests with 75%+ code coverage
- **Fault Tolerance**: Circuit breakers, retries, fallbacks, and monitoring for resilient operation
- **Multiple Implementation Approaches**: Both procedural and OOP implementations for learning

## 🚀 Features

### Core Financial Intelligence
- **Real-time Stock Data**: Get current stock prices, fundamentals, and analyst recommendations
- **Company News**: Access latest news and press releases for companies
- **Web Search Integration**: Combine financial data with broader web search results
- **Multi-Agent Architecture**: Specialized agents for different types of financial queries

### Enterprise Architecture
- **Domain Driven Design**: Clean separation of business logic and infrastructure
- **Test Driven Development**: 48 comprehensive tests with code coverage reporting
- **Fault Tolerance**: Circuit breakers, retries, and fallbacks for resilient operation
- **Monitoring & Alerting**: Real-time health metrics and system observability

### Implementation Approaches
- **Abstract Factory Pattern**: Enterprise-grade OOP design with extensible agent creation
- **Interactive Playground**: Web-based interface using Factory Pattern
- **Streaming Responses**: Real-time response streaming for better user experience
- **Dual Implementation**: Both procedural and DDD approaches for learning

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

### Fault Tolerance & Resilience
- **Circuit Breakers**: Automatic failure detection and recovery
- **Retry Mechanisms**: Exponential backoff for transient failures
- **Fallback Handlers**: Graceful degradation with cached data
- **Health Monitoring**: Real-time system observability and alerting

## 🏗️ Architecture & Design Patterns

This project demonstrates **enterprise-grade software engineering** with multiple architectural approaches:

### Domain Driven Design (DDD) Architecture

**Clean Architecture** with clear separation of concerns:

```
📁 domain/           # Business logic and domain models
📁 application/      # Use cases and application services
📁 infrastructure/   # External integrations and frameworks
📁 bootstrap.py      # Dependency injection and configuration
```

**Key DDD Benefits**:
- **Business Focus**: Domain entities represent real financial concepts
- **Testability**: Clear boundaries enable comprehensive testing
- **Maintainability**: Changes isolated to appropriate layers
- **Extensibility**: New features follow established patterns

### Fault Tolerance & Resilience

**Enterprise-grade reliability** with proven patterns:

- **Circuit Breakers**: Prevent cascading failures
- **Retry Mechanisms**: Handle transient failures with exponential backoff
- **Fallback Handlers**: Graceful degradation with cached data
- **Monitoring & Alerting**: Real-time health metrics and alerts

### Traditional OOP Implementation

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

## 🧪 Testing & Quality Assurance

### Comprehensive Test Suite
```bash
# Run all tests with coverage
pytest tests/ --cov --cov-report=html

# Run specific test categories
pytest tests/test_domain_entities.py    # Domain model tests
pytest tests/test_domain_services.py    # Business logic tests
pytest tests/test_application_services.py  # Application layer tests
pytest tests/test_integration.py        # Integration tests
```

### Test Coverage
- **48 Unit & Integration Tests**: Complete coverage of domain logic
- **75%+ Code Coverage**: Focused on critical business logic
- **TDD Approach**: Tests written before implementation
- **CI/CD Ready**: Automated testing pipeline

### Quality Metrics
- **SOLID Principles**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion
- **DRY Principle**: No code duplication across implementations
- **Clean Code**: Readable, maintainable, well-documented code
- **Design Patterns**: Abstract Factory, Strategy, Observer, and more

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
financial-ai-agent/
├── 📄 README.md                    # Project documentation
├── 📋 requirements.txt             # Python dependencies
├── 🔐 .env                        # Environment variables (create this)
├── 🚫 .gitignore                  # Git exclusion rules
├── 📊 pytest.ini                  # Test configuration
├── ⚙️ setup.cfg                   # Coverage configuration
│
├── 🏗️ Architecture (DDD)
│   ├── domain/                    # Business domain layer
│   │   ├── __init__.py
│   │   ├── entities.py            # Domain entities and value objects
│   │   ├── services.py            # Domain services and business logic
│   │   └── repositories.py        # Repository interfaces
│   ├── application/               # Application layer
│   │   ├── __init__.py
│   │   └── services.py            # Use cases and application services
│   ├── infrastructure/            # Infrastructure layer
│   │   ├── __init__.py
│   │   ├── yfinance_adapter.py    # External API integrations
│   │   ├── fault_tolerance.py     # Resilience patterns
│   │   └── monitoring.py          # Health monitoring
│   └── bootstrap.py               # Dependency injection
│
├── 🧪 Testing
│   └── tests/                     # Comprehensive test suite
│       ├── __init__.py
│       ├── test_domain_entities.py
│       ├── test_domain_services.py
│       ├── test_application_services.py
│       └── test_integration.py
│
├── 📊 Documentation & Diagrams
│   └── diagrams/                  # Architecture diagrams
│       ├── sequence_diagrams.puml
│       ├── component_diagrams.puml
│       ├── deployment_diagram.puml
│       ├── package_diagram.puml
│       ├── multi_agent_sequence.puml
│       ├── fault_tolerance_sequence.puml
│       └── fault_tolerance_overview.puml
│
├── 🔧 Legacy Implementations
│   ├── financial_agent.py         # Original procedural implementation
│   └── financial_agent_oop.py     # Traditional OOP with Factory Pattern
│
├── 🌐 Web Interface
│   └── playground.py              # Web playground using Factory Pattern
│
├── 📚 Educational Content
│   ├── demo_oop.py                # Factory Pattern demonstration
│   ├── chat_example.txt           # Example conversations
│   ├── ARTIFACTS_SUMMARY.md       # Project summary
│   └── FAULT_TOLERANCE_README.md  # Fault tolerance documentation
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

This project demonstrates **enterprise software engineering** practices:

### Architecture & Design
- **Domain Driven Design (DDD)**: Strategic and tactical DDD patterns
- **Clean Architecture**: Layered architecture with clear boundaries
- **SOLID Principles**: Professional OOP design principles
- **Design Patterns**: Abstract Factory, Strategy, Observer, and more

### Development Practices
- **Test Driven Development (TDD)**: Writing tests before implementation
- **Code Coverage**: Comprehensive testing with coverage reporting
- **Continuous Integration**: Automated testing pipelines
- **Professional Code Organization**: Modular, maintainable codebase

### Reliability Engineering
- **Fault Tolerance Patterns**: Circuit breakers, retries, fallbacks
- **Resilience Engineering**: Handling failures gracefully
- **Monitoring & Observability**: System health and metrics
- **Error Handling**: Comprehensive error management

### Technical Skills
- **Multi-agent AI systems** with specialized agents
- **Web development** with FastAPI and Uvicorn
- **Financial data APIs** integration (YFinance, web search)
- **Python ecosystem** mastery (typing, dataclasses, testing)

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Not financial advice. Always do your own research and consult with financial professionals before making investment decisions.

## 🔍 Example Output

The agent provides structured responses including:

- Tabular analyst recommendations
- Summarized news headlines
- Source attribution
- Combined analysis from multiple data sources

See `chat_example.txt` for detailed example interactions.

## 📊 Architecture Diagrams

### Available Diagrams
- **Sequence Diagrams**: Request flow through multi-agent system
- **Component Diagrams**: DDD layered architecture
- **Deployment Diagrams**: System deployment and relationships
- **Package Diagrams**: Python module organization
- **Fault Tolerance Diagrams**: Resilience patterns and error handling

### Viewing Diagrams
```bash
# Install PlantUML viewer (optional)
# Diagrams are in diagrams/*.puml files
# Can be viewed with PlantUML plugins or online viewers
```

## 🔍 Monitoring & Health Checks

### System Health
```python
from infrastructure.monitoring import get_monitoring_service

monitoring = get_monitoring_service()
health = monitoring.get_system_health()
alerts = monitoring.get_alerts()
```

### Circuit Breaker Status
- Monitor API health in real-time
- Automatic failure detection and recovery
- Configurable thresholds and timeouts

## 🏆 Key Achievements

### 🏗️ Architecture Excellence
- ✅ **Domain Driven Design**: Complete DDD implementation with clean boundaries
- ✅ **Layered Architecture**: Domain, Application, Infrastructure separation
- ✅ **Multiple Design Patterns**: Abstract Factory, Strategy, Observer, Repository
- ✅ **SOLID Principles**: Professional OOP design throughout

### 🧪 Quality Assurance
- ✅ **Test Driven Development**: 48 comprehensive tests with TDD approach
- ✅ **Code Coverage**: 75%+ coverage with automated reporting
- ✅ **Integration Testing**: End-to-end system validation
- ✅ **Quality Metrics**: Automated testing and coverage pipelines

### 🛡️ Reliability Engineering
- ✅ **Fault Tolerance**: Circuit breakers, retries, fallbacks implementation
- ✅ **Resilience Patterns**: Enterprise-grade error handling and recovery
- ✅ **Monitoring System**: Real-time health metrics and alerting
- ✅ **Graceful Degradation**: System continues operating during failures

### 🚀 Development Practices
- ✅ **Multiple Implementations**: Procedural, OOP Factory, and DDD approaches
- ✅ **Web Deployment**: Interactive playground with streaming responses
- ✅ **Professional Documentation**: Comprehensive README, diagrams, and guides
- ✅ **Version Control**: Git with proper branching and .gitignore
- ✅ **Environment Management**: Virtual environments and dependency management
