# Financial AI Agent

A powerful multi-agent AI system that combines financial data analysis with web search capabilities to provide comprehensive market intelligence and investment insights.

## 🚀 Features

- **Real-time Stock Data**: Get current stock prices, fundamentals, and analyst recommendations
- **Company News**: Access latest news and press releases for companies
- **Web Search Integration**: Combine financial data with broader web search results
- **Multi-Agent Architecture**: Specialized agents for different types of financial queries
- **Interactive Playground**: Web-based interface for easy interaction
- **Streaming Responses**: Real-time response streaming for better user experience

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

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```env
PHI_API_KEY=your_phi_api_key
GROQ_API_KEY=your_groq_api_key
```

## 🚀 Usage

### Command Line Interface

Run the main financial agent:
```bash
python financial_agent.py
```

### Interactive Playground

Launch the web interface:
```bash
python playground.py
```

This will start a local web server where you can interact with the agents through a user-friendly interface.

## 💡 Example Queries

- "Summarize analyst recommendations and share the latest news for NVDA"
- "Compare Tesla and NVIDIA analyst recommendations"
- "Get current stock price for AAPL"
- "What are the fundamentals for Microsoft?"

## 📁 Project Structure

```
financial_agent/
├── financial_agent.py      # Main multi-agent implementation
├── playground.py           # Web playground interface
├── requirements.txt        # Python dependencies
├── chat_example.txt        # Example conversation logs
├── README.md              # This file
└── venv/                  # Virtual environment
```

## 🏗️ Architecture

### Agents

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
- **Streamlit/Uvicorn**: Web server for playground

## 🔧 Configuration

The agents are configured with the following models and tools:

- **Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Financial Tools**: YFinance (price, fundamentals, recommendations, news)
- **Search Tools**: DuckDuckGo web search

## 📝 Dependencies

Key dependencies include:
- `phidata`: Multi-agent framework
- `groq`: AI model provider
- `yfinance`: Financial data
- `ddgs`: DuckDuckGo search
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `python-dotenv`: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Not financial advice. Always do your own research and consult with financial professionals before making investment decisions.

## 🔍 Example Output

The agent provides structured responses including:

- Tabular analyst recommendations
- Summarized news headlines
- Source attribution
- Combined analysis from multiple data sources

See `chat_example.txt` for detailed example interactions.
