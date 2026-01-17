"""Unit tests for domain services."""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from unittest.mock import Mock

from domain.entities import (
    StockSymbol, Price, Stock, AnalystRecommendation,
    CompanyNews, Query, Recommendation
)
from domain.services import (
    QueryAnalysisService, RecommendationAnalysisService,
    NewsAnalysisService, QueryProcessingService
)


class TestQueryAnalysisService:
    """Test QueryAnalysisService."""

    def test_analyze_query_with_stock_symbols(self):
        """Test query analysis with stock symbols."""
        service = QueryAnalysisService()

        query = service.analyze_query("What is the price of AAPL and TSLA?")

        assert query.content == "What is the price of AAPL and TSLA?"
        assert len(query.symbols) == 2
        assert query.symbols[0].symbol == "AAPL"
        assert query.symbols[1].symbol == "TSLA"
        assert query.is_multi_symbol_query()

    def test_analyze_query_price_type(self):
        """Test query type classification for price queries."""
        service = QueryAnalysisService()

        query = service.analyze_query("Get current price for MSFT")
        assert query.query_type == "stock_price"

    def test_analyze_query_recommendations_type(self):
        """Test query type classification for recommendation queries."""
        service = QueryAnalysisService()

        query = service.analyze_query("What are analyst recommendations for NVDA?")
        assert query.query_type == "analyst_recommendations"

    def test_analyze_query_news_type(self):
        """Test query type classification for news queries."""
        service = QueryAnalysisService()

        query = service.analyze_query("Latest news about AAPL")
        assert query.query_type == "news"

    def test_analyze_query_comparison_type(self):
        """Test query type classification for comparison queries."""
        service = QueryAnalysisService()

        query = service.analyze_query("Compare AAPL and GOOGL stock prices")
        assert query.query_type == "comparison"

    def test_analyze_query_fundamentals_type(self):
        """Test query type classification for fundamentals queries."""
        service = QueryAnalysisService()

        query = service.analyze_query("What are the fundamentals for MSFT?")
        assert query.query_type == "fundamentals"


class TestRecommendationAnalysisService:
    """Test RecommendationAnalysisService."""

    def test_analyze_recommendations_buy_consensus(self):
        """Test recommendation analysis with buy consensus."""
        service = RecommendationAnalysisService()

        recommendations = [
            AnalystRecommendation(StockSymbol("AAPL"), "Firm1", Recommendation.STRONG_BUY),
            AnalystRecommendation(StockSymbol("AAPL"), "Firm2", Recommendation.BUY),
            AnalystRecommendation(StockSymbol("AAPL"), "Firm3", Recommendation.BUY),
        ]

        analysis = service.analyze_recommendations(recommendations)

        assert analysis["total"] == 3
        assert analysis["buy_ratings"] == 3
        assert analysis["hold_ratings"] == 0
        assert analysis["sell_ratings"] == 0
        assert analysis["consensus"] == "Strong Buy"

    def test_analyze_recommendations_sell_consensus(self):
        """Test recommendation analysis with sell consensus."""
        service = RecommendationAnalysisService()

        recommendations = [
            AnalystRecommendation(StockSymbol("AAPL"), "Firm1", Recommendation.SELL),
            AnalystRecommendation(StockSymbol("AAPL"), "Firm2", Recommendation.STRONG_SELL),
        ]

        analysis = service.analyze_recommendations(recommendations)

        assert analysis["total"] == 2
        assert analysis["sell_ratings"] == 2
        assert analysis["consensus"] == "Sell"

    def test_analyze_recommendations_with_targets(self):
        """Test recommendation analysis with price targets."""
        service = RecommendationAnalysisService()

        recommendations = [
            AnalystRecommendation(StockSymbol("AAPL"), "Firm1", Recommendation.BUY,
                                price_target=Price(Decimal("150"))),
            AnalystRecommendation(StockSymbol("AAPL"), "Firm2", Recommendation.BUY,
                                price_target=Price(Decimal("160"))),
        ]

        analysis = service.analyze_recommendations(recommendations)

        assert analysis["average_target"] == 155.0  # (150 + 160) / 2

    def test_analyze_empty_recommendations(self):
        """Test recommendation analysis with no recommendations."""
        service = RecommendationAnalysisService()

        analysis = service.analyze_recommendations([])

        assert analysis["total"] == 0
        assert analysis["consensus"] is None
        assert analysis["average_target"] is None


class TestNewsAnalysisService:
    """Test NewsAnalysisService."""

    def test_summarize_news(self):
        """Test news summarization."""
        service = NewsAnalysisService()

        news_items = [
            CompanyNews(
                StockSymbol("AAPL"),
                "Apple Q4 Results Beat Expectations",
                "Apple reported revenue of $25B",
                "Bloomberg",
                "https://bloomberg.com",
                datetime.now()
            ),
            CompanyNews(
                StockSymbol("AAPL"),
                "Apple Stock Rises on Earnings",
                "Shares up 5% after earnings",
                "Reuters",
                "https://reuters.com",
                datetime.now()
            ),
        ]

        summary = service.summarize_news(news_items, max_items=2)

        assert "Apple Q4 Results" in summary
        assert "Apple Stock Rises" in summary
        assert "Bloomberg" in summary

    def test_summarize_empty_news(self):
        """Test news summarization with no news."""
        service = NewsAnalysisService()

        summary = service.summarize_news([])
        assert summary == "No recent news available."

    def test_analyze_sentiment_positive(self):
        """Test sentiment analysis with positive news."""
        service = NewsAnalysisService()

        news_items = [
            CompanyNews(StockSymbol("AAPL"), "Title1", sentiment="positive"),
            CompanyNews(StockSymbol("AAPL"), "Title2", sentiment="positive"),
            CompanyNews(StockSymbol("AAPL"), "Title3", sentiment="neutral"),
        ]

        sentiment = service.analyze_sentiment(news_items)

        assert sentiment["sentiment"] == "positive"
        assert sentiment["confidence"] > 0.5

    def test_analyze_sentiment_negative(self):
        """Test sentiment analysis with negative news."""
        service = NewsAnalysisService()

        news_items = [
            CompanyNews(StockSymbol("AAPL"), "Title1", sentiment="negative"),
            CompanyNews(StockSymbol("AAPL"), "Title2", sentiment="negative"),
        ]

        sentiment = service.analyze_sentiment(news_items)

        assert sentiment["sentiment"] == "negative"
        assert sentiment["confidence"] == 1.0

    def test_analyze_sentiment_neutral(self):
        """Test sentiment analysis with neutral/mixed news."""
        service = NewsAnalysisService()

        news_items = [
            CompanyNews(StockSymbol("AAPL"), "Title1", sentiment="positive"),
            CompanyNews(StockSymbol("AAPL"), "Title2", sentiment="negative"),
            CompanyNews(StockSymbol("AAPL"), "Title3", sentiment="neutral"),
        ]

        sentiment = service.analyze_sentiment(news_items)

        assert sentiment["sentiment"] == "neutral"


class TestQueryProcessingService:
    """Test QueryProcessingService."""

    def test_process_price_query(self):
        """Test processing a price query."""
        # Mock stock service
        mock_stock_service = Mock()
        symbol = StockSymbol("AAPL")
        stock = Stock(symbol=symbol, current_price=Price(Decimal("150.00")))
        mock_stock_service.get_stock_info.return_value = stock

        # Create service
        query_analyzer = QueryAnalysisService()
        rec_analyzer = RecommendationAnalysisService()
        news_analyzer = NewsAnalysisService()

        service = QueryProcessingService(
            mock_stock_service, query_analyzer, rec_analyzer, news_analyzer
        )

        result = service.process_query("What is the price of AAPL?")

        assert result.success
        assert "Current price of AAPL: $150.00" in result.response
        assert result.processing_time is not None

    def test_process_recommendations_query(self):
        """Test processing a recommendations query."""
        # Mock services
        mock_stock_service = Mock()
        mock_stock_service.get_analyst_recommendations.return_value = [
            AnalystRecommendation(StockSymbol("AAPL"), "Firm1", Recommendation.BUY),
            AnalystRecommendation(StockSymbol("AAPL"), "Firm2", Recommendation.STRONG_BUY),
        ]

        # Create service
        query_analyzer = QueryAnalysisService()
        rec_analyzer = RecommendationAnalysisService()
        news_analyzer = NewsAnalysisService()

        service = QueryProcessingService(
            mock_stock_service, query_analyzer, rec_analyzer, news_analyzer
        )

        result = service.process_query("Get analyst recommendations for AAPL")

        assert result.success
        assert "Analyst Recommendations for AAPL" in result.response
        assert "Strong Buy" in result.response

    def test_process_query_with_error(self):
        """Test processing a query that causes an error."""
        # Mock stock service to raise exception
        mock_stock_service = Mock()
        mock_stock_service.get_stock_info.side_effect = Exception("API Error")

        # Create service
        query_analyzer = QueryAnalysisService()
        rec_analyzer = RecommendationAnalysisService()
        news_analyzer = NewsAnalysisService()

        service = QueryProcessingService(
            mock_stock_service, query_analyzer, rec_analyzer, news_analyzer
        )

        result = service.process_query("What is the price of AAPL?")  # Use a valid symbol

        assert not result.success
        assert result.error_message == "API Error"
        assert result.processing_time is not None
