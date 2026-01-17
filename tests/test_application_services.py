"""Unit tests for application services."""

import pytest
from decimal import Decimal
from unittest.mock import Mock

from domain.entities import StockSymbol, Price, Stock, AnalystRecommendation, Recommendation
from domain.repositories import (
    InMemoryStockRepository, InMemoryAnalystRecommendationRepository,
    InMemoryCompanyNewsRepository, InMemoryQueryResultRepository
)
from application.services import (
    FinancialAnalysisService, QueryProcessingApplicationService, AnalyticsService
)


class TestFinancialAnalysisService:
    """Test FinancialAnalysisService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.stock_repo = InMemoryStockRepository()
        self.recommendation_repo = InMemoryAnalystRecommendationRepository()
        self.news_repo = InMemoryCompanyNewsRepository()
        self.query_repo = InMemoryQueryResultRepository()

        self.service = FinancialAnalysisService(
            self.stock_repo, self.recommendation_repo,
            self.news_repo, self.query_repo
        )

    def test_get_stock_analysis_complete(self):
        """Test getting complete stock analysis."""
        # Setup test data
        symbol = StockSymbol("AAPL")
        stock = Stock(
            symbol=symbol,
            name="Apple Inc.",
            current_price=Price(Decimal("150.00")),
            sector="Technology"
        )
        self.stock_repo.save(stock)

        recommendations = [
            AnalystRecommendation(symbol, "Firm1", Recommendation.BUY),
            AnalystRecommendation(symbol, "Firm2", Recommendation.STRONG_BUY),
        ]
        self.recommendation_repo.save_all(recommendations)

        # Execute
        analysis = self.service.get_stock_analysis(symbol)

        # Assert
        assert analysis is not None
        assert analysis["stock"].name == "Apple Inc."
        assert len(analysis["recommendations"]) == 2
        assert analysis["recommendation_analysis"]["buy_ratings"] == 2
        assert analysis["recommendation_analysis"]["consensus"] == "Strong Buy"

    def test_get_stock_analysis_not_found(self):
        """Test getting analysis for non-existent stock."""
        symbol = StockSymbol("INVALID")

        analysis = self.service.get_stock_analysis(symbol)

        assert analysis is None


class TestQueryProcessingApplicationService:
    """Test QueryProcessingApplicationService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.stock_repo = InMemoryStockRepository()
        self.recommendation_repo = InMemoryAnalystRecommendationRepository()
        self.news_repo = InMemoryCompanyNewsRepository()
        self.query_repo = InMemoryQueryResultRepository()

        self.service = QueryProcessingApplicationService(
            self.stock_repo, self.recommendation_repo,
            self.news_repo, self.query_repo
        )

    def test_process_price_query(self):
        """Test processing a price query."""
        # Setup test data
        symbol = StockSymbol("AAPL")
        stock = Stock(symbol=symbol, current_price=Price(Decimal("150.00")))
        self.stock_repo.save(stock)

        # Execute
        result = self.service.process_query("What is the price of AAPL?")

        # Assert
        assert result.success
        assert "Current price of AAPL: $150.00" in result.response
        assert result.processing_time >= 0

        # Check that result was saved
        saved_results = self.query_repo.find_recent(1)
        assert len(saved_results) == 1
        assert saved_results[0].query.content == "What is the price of AAPL?"

    def test_process_recommendations_query(self):
        """Test processing a recommendations query."""
        # Setup test data
        symbol = StockSymbol("AAPL")
        recommendations = [
            AnalystRecommendation(symbol, "Goldman Sachs", Recommendation.BUY,
                                price_target=Price(Decimal("180"))),
            AnalystRecommendation(symbol, "Morgan Stanley", Recommendation.STRONG_BUY,
                                price_target=Price(Decimal("190"))),
        ]
        self.recommendation_repo.save_all(recommendations)

        # Execute
        result = self.service.process_query("Get analyst recommendations for AAPL")

        # Assert
        assert result.success
        assert "Analyst Recommendations for AAPL" in result.response
        assert "Strong Buy" in result.response

    def test_process_general_query(self):
        """Test processing a general query without symbols."""
        result = self.service.process_query("What is the stock market doing today?")

        assert result.success
        assert "understand you're asking about" in result.response

    def test_process_query_with_error(self):
        """Test processing a query that causes an error."""
        # Make stock repo raise an exception
        original_find = self.stock_repo.find_by_symbol
        self.stock_repo.find_by_symbol = Mock(side_effect=Exception("Database error"))

        result = self.service.process_query("What is the price of AAPL?")

        assert not result.success
        assert result.error_message == "Database error"

        # Restore original method
        self.stock_repo.find_by_symbol = original_find

    def test_get_stock_price_implementation(self):
        """Test StockDataService protocol implementation."""
        # Setup
        symbol = StockSymbol("AAPL")
        stock = Stock(symbol=symbol, current_price=Price(Decimal("150.00")))
        self.stock_repo.save(stock)

        # Test the protocol method
        price = self.service.get_stock_price(symbol)
        assert price == 150.0

    def test_get_stock_info_implementation(self):
        """Test get_stock_info protocol implementation."""
        symbol = StockSymbol("AAPL")
        stock = Stock(symbol=symbol, current_price=Price(Decimal("150.00")))
        self.stock_repo.save(stock)

        retrieved_stock = self.service.get_stock_info(symbol)
        assert retrieved_stock.current_price.value == Decimal("150.00")


class TestAnalyticsService:
    """Test AnalyticsService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.query_repo = InMemoryQueryResultRepository()
        self.service = AnalyticsService(self.query_repo)

    def test_get_query_statistics_empty(self):
        """Test getting statistics with no queries."""
        stats = self.service.get_query_statistics()

        assert stats["total_queries"] == 0
        assert stats["successful_queries"] == 0
        assert stats["success_rate"] == 0.0

    def test_get_query_statistics_with_data(self):
        """Test getting statistics with query data."""
        from domain.entities import Query, QueryResult

        # Add some test results
        successful_query = Query("Successful query")
        successful_result = QueryResult(successful_query, "Response", success=True, processing_time=1.0)
        self.query_repo.save(successful_result)

        failed_query = Query("Failed query")
        failed_result = QueryResult(failed_query, "", success=False, error_message="Error", processing_time=0.5)
        self.query_repo.save(failed_result)

        # Get statistics
        stats = self.service.get_query_statistics()

        assert stats["total_queries"] == 2
        assert stats["successful_queries"] == 1
        assert stats["failed_queries"] == 1
        assert stats["success_rate"] == 0.5
        assert abs(stats["average_processing_time"] - 0.75) < 0.01  # (1.0 + 0.5) / 2

    def test_get_popular_symbols(self):
        """Test getting popular symbols analytics."""
        from domain.entities import Query, QueryResult

        # Create queries with different symbols
        queries = [
            Query("AAPL query", symbols=[StockSymbol("AAPL")]),
            Query("AAPL again", symbols=[StockSymbol("AAPL")]),
            Query("TSLA query", symbols=[StockSymbol("TSLA")]),
        ]

        for query in queries:
            result = QueryResult(query, "Response", success=True)
            self.query_repo.save(result)

        popular = self.service.get_popular_symbols(5)

        assert len(popular) == 2
        assert popular[0] == ("AAPL", 2)  # AAPL appears twice
        assert popular[1] == ("TSLA", 1)  # TSLA appears once
