"""Domain services for the Financial AI Agent system."""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from .entities import (
    Stock, StockSymbol, AnalystRecommendation,
    CompanyNews, Query, QueryResult, Recommendation
)


class StockDataService(Protocol):
    """Protocol for stock data operations."""

    def get_stock_info(self, symbol: StockSymbol) -> Optional[Stock]:
        """Get comprehensive stock information."""
        ...

    def get_stock_price(self, symbol: StockSymbol) -> Optional[float]:
        """Get current stock price."""
        ...

    def get_analyst_recommendations(self, symbol: StockSymbol) -> List[AnalystRecommendation]:
        """Get analyst recommendations for a stock."""
        ...

    def get_company_news(self, symbol: StockSymbol, limit: int = 10) -> List[CompanyNews]:
        """Get recent company news."""
        ...


class QueryAnalysisService:
    """Domain service for analyzing and categorizing queries."""

    def analyze_query(self, query_text: str) -> Query:
        """Analyze a query text and create a Query entity."""
        query = Query(content=query_text)

        # Extract stock symbols from query
        symbols = self._extract_symbols(query_text)
        for symbol in symbols:
            query.add_symbol(symbol)

        # Determine query type
        query.query_type = self._classify_query_type(query_text, symbols)

        return query

    def _extract_symbols(self, text: str) -> List[StockSymbol]:
        """Extract stock symbols from query text."""
        # Simple extraction logic - can be enhanced with NLP
        common_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'META', 'AMZN', 'NFLX']
        found_symbols = []

        text_upper = text.upper()
        for symbol in common_symbols:
            if symbol in text_upper:
                try:
                    found_symbols.append(StockSymbol(symbol))
                except ValueError:
                    continue  # Invalid symbol format

        return found_symbols

    def _classify_query_type(self, text: str, symbols: List[StockSymbol]) -> str:
        """Classify the type of query based on content."""
        text_lower = text.lower()

        if "compare" in text_lower or (len(symbols) > 1 and ("price" in text_lower or "vs" in text_lower)):
            return "comparison"
        elif "price" in text_lower or "current" in text_lower:
            return "stock_price"
        elif "analyst" in text_lower or "recommendation" in text_lower:
            return "analyst_recommendations"
        elif "news" in text_lower or "latest" in text_lower:
            return "news"
        elif "fundamental" in text_lower or "pe ratio" in text_lower:
            return "fundamentals"
        else:
            return "general"


class RecommendationAnalysisService:
    """Domain service for analyzing analyst recommendations."""

    def analyze_recommendations(self, recommendations: List[AnalystRecommendation]) -> dict:
        """Analyze a list of recommendations and return summary statistics."""
        if not recommendations:
            return {
                "total": 0,
                "buy_ratings": 0,
                "hold_ratings": 0,
                "sell_ratings": 0,
                "average_target": None,
                "consensus": None
            }

        buy_count = sum(1 for r in recommendations if r.is_bullish())
        sell_count = sum(1 for r in recommendations if r.is_bearish())
        hold_count = len(recommendations) - buy_count - sell_count

        # Calculate average price target
        targets = [r.price_target.value for r in recommendations if r.price_target]
        avg_target = sum(targets) / len(targets) if targets else None

        # Determine consensus
        consensus = self._calculate_consensus(buy_count, hold_count, sell_count, len(recommendations))

        return {
            "total": len(recommendations),
            "buy_ratings": buy_count,
            "hold_ratings": hold_count,
            "sell_ratings": sell_count,
            "average_target": avg_target,
            "consensus": consensus
        }

    def _calculate_consensus(self, buy: int, hold: int, sell: int, total: int) -> str:
        """Calculate consensus recommendation."""
        buy_ratio = buy / total
        sell_ratio = sell / total

        if buy_ratio >= 0.6:
            return "Strong Buy"
        elif buy_ratio >= 0.4:
            return "Buy"
        elif sell_ratio >= 0.4:
            return "Sell"
        else:
            return "Hold"


class NewsAnalysisService:
    """Domain service for analyzing company news."""

    def summarize_news(self, news_list: List[CompanyNews], max_items: int = 5) -> str:
        """Create a summary of recent news."""
        if not news_list:
            return "No recent news available."

        recent_news = sorted(news_list, key=lambda x: x.published_date, reverse=True)[:max_items]

        summary_parts = []
        for news in recent_news:
            date_str = news.published_date.strftime("%Y-%m-%d")
            summary_parts.append(f"• {date_str}: {news.title} ({news.source})")
            if news.summary:
                summary_parts.append(f"  {news.summary[:100]}...")

        return "\n".join(summary_parts)

    def analyze_sentiment(self, news_list: List[CompanyNews]) -> dict:
        """Analyze overall sentiment from news."""
        if not news_list:
            return {"sentiment": "neutral", "confidence": 0.0}

        sentiments = [n.sentiment for n in news_list if n.sentiment]

        if not sentiments:
            return {"sentiment": "neutral", "confidence": 0.0}

        positive = sentiments.count("positive")
        negative = sentiments.count("negative")
        neutral = sentiments.count("neutral")

        total = len(sentiments)
        if positive > negative and positive > neutral:
            return {"sentiment": "positive", "confidence": positive / total}
        elif negative > positive and negative > neutral:
            return {"sentiment": "negative", "confidence": negative / total}
        else:
            return {"sentiment": "neutral", "confidence": neutral / total}


class QueryProcessingService:
    """Domain service for processing queries and generating responses."""

    def __init__(self,
                 stock_service: StockDataService,
                 query_analyzer: QueryAnalysisService,
                 recommendation_analyzer: RecommendationAnalysisService,
                 news_analyzer: NewsAnalysisService):
        self.stock_service = stock_service
        self.query_analyzer = query_analyzer
        self.recommendation_analyzer = recommendation_analyzer
        self.news_analyzer = news_analyzer

    def process_query(self, query_text: str) -> QueryResult:
        """Process a query and return results."""
        import time
        start_time = time.time()

        try:
            # Analyze the query
            query = self.query_analyzer.analyze_query(query_text)
            result = QueryResult(query=query)

            # Process based on query type
            if query.symbols:
                response = self._process_symbol_query(query)
            else:
                response = self._process_general_query(query)

            result.response = response
            result.processing_time = time.time() - start_time

            return result

        except Exception as e:
            error_result = QueryResult(
                query=Query(content=query_text),
                response="",
                success=False,
                error_message=str(e)
            )
            error_result.processing_time = time.time() - start_time
            return error_result

    def _process_symbol_query(self, query: Query) -> str:
        """Process a query that involves stock symbols."""
        responses = []

        for symbol in query.symbols:
            symbol_responses = []

            if query.query_type == "stock_price":
                stock = self.stock_service.get_stock_info(symbol)
                if stock and stock.current_price:
                    symbol_responses.append(f"Current price of {symbol.symbol}: {stock.current_price.formatted()}")

            elif query.query_type == "analyst_recommendations":
                recommendations = self.stock_service.get_analyst_recommendations(symbol)
                if recommendations:
                    analysis = self.recommendation_analyzer.analyze_recommendations(recommendations)
                    symbol_responses.append(f"Analyst Recommendations for {symbol.symbol}:")
                    symbol_responses.append(f"Consensus: {analysis['consensus']}")
                    symbol_responses.append(f"Buy: {analysis['buy_ratings']}, Hold: {analysis['hold_ratings']}, Sell: {analysis['sell_ratings']}")

            elif query.query_type == "news":
                news = self.stock_service.get_company_news(symbol)
                if news:
                    news_summary = self.news_analyzer.summarize_news(news)
                    symbol_responses.append(f"Recent News for {symbol.symbol}:")
                    symbol_responses.append(news_summary)

            else:  # general or fundamentals
                stock = self.stock_service.get_stock_info(symbol)
                if stock:
                    symbol_responses.append(f"Fundamentals for {symbol.symbol}:")
                    if stock.market_cap:
                        symbol_responses.append(f"Market Cap: {stock.market_cap.formatted()}")
                    if stock.pe_ratio:
                        symbol_responses.append(f"P/E Ratio: {stock.pe_ratio}")
                    if stock.sector:
                        symbol_responses.append(f"Sector: {stock.sector}")

            responses.extend(symbol_responses)

        return "\n\n".join(responses) if responses else "No information found for the requested symbols."

    def _process_general_query(self, query: Query) -> str:
        """Process a general query without specific symbols."""
        # For now, return a placeholder response
        # In a full implementation, this would use web search or general AI
        return f"I understand you're asking about: {query.content}. For financial queries, please specify stock symbols for detailed analysis."
