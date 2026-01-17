"""Integration tests for the Financial AI Agent system."""

import pytest
from decimal import Decimal

from domain.entities import StockSymbol, Price, Stock
from domain.repositories import (
    InMemoryStockRepository, InMemoryAnalystRecommendationRepository,
    InMemoryCompanyNewsRepository, InMemoryQueryResultRepository
)
from application.services import QueryProcessingApplicationService


class TestSystemIntegration:
    """Integration tests for the complete system."""

    def test_full_query_processing_flow(self):
        """Test the complete flow from query to result."""
        # Setup repositories
        stock_repo = InMemoryStockRepository()
        recommendation_repo = InMemoryAnalystRecommendationRepository()
        news_repo = InMemoryCompanyNewsRepository()
        query_repo = InMemoryQueryResultRepository()

        service = QueryProcessingApplicationService(
            stock_repo, recommendation_repo, news_repo, query_repo
        )

        # Setup test data
        symbol = StockSymbol("AAPL")
        stock = Stock(
            symbol=symbol,
            name="Apple Inc.",
            current_price=Price(Decimal("150.00")),
            sector="Technology"
        )
        stock_repo.save(stock)

        # Process query
        result = service.process_query("What is the price of AAPL?")

        # Assert
        assert result.success
        assert "Current price of AAPL: $150.00" in result.response
        assert result.processing_time >= 0

    def test_multi_symbol_query_processing(self):
        """Test processing queries with multiple symbols."""
        # Setup repositories
        stock_repo = InMemoryStockRepository()
        recommendation_repo = InMemoryAnalystRecommendationRepository()
        news_repo = InMemoryCompanyNewsRepository()
        query_repo = InMemoryQueryResultRepository()

        service = QueryProcessingApplicationService(
            stock_repo, recommendation_repo, news_repo, query_repo
        )

        # Setup test data for multiple stocks
        stocks = [
            Stock(StockSymbol("AAPL"), current_price=Price(Decimal("150.00"))),
            Stock(StockSymbol("TSLA"), current_price=Price(Decimal("250.00"))),
        ]

        for stock in stocks:
            stock_repo.save(stock)

        # Process multi-symbol query
        result = service.process_query("Compare prices of AAPL and TSLA")

        assert result.success
        assert "AAPL" in result.response
        assert "TSLA" in result.response

    def test_analytics_integration(self):
        """Test analytics service integration."""
        # Setup repositories
        stock_repo = InMemoryStockRepository()
        recommendation_repo = InMemoryAnalystRecommendationRepository()
        news_repo = InMemoryCompanyNewsRepository()
        query_repo = InMemoryQueryResultRepository()

        service = QueryProcessingApplicationService(
            stock_repo, recommendation_repo, news_repo, query_repo
        )

        from application.services import AnalyticsService
        analytics = AnalyticsService(query_repo)

        # Process several queries
        queries = [
            "Price of AAPL",
            "News about TSLA",
            "Recommendations for MSFT"
        ]

        for query in queries:
            service.process_query(query)

        # Get analytics
        stats = analytics.get_query_statistics()

        assert stats["total_queries"] == 3
        assert stats["successful_queries"] == 3  # Assuming all succeed with mock data

    def test_error_handling_integration(self):
        """Test error handling across the system."""
        # Setup repositories
        stock_repo = InMemoryStockRepository()
        recommendation_repo = InMemoryAnalystRecommendationRepository()
        news_repo = InMemoryCompanyNewsRepository()
        query_repo = InMemoryQueryResultRepository()

        service = QueryProcessingApplicationService(
            stock_repo, recommendation_repo, news_repo, query_repo
        )

        # Process query that should fail gracefully
        result = service.process_query("Query with invalid symbol XYZ123456789")

        # Should still return a result, even if with limited information
        assert result is not None
        assert isinstance(result.processing_time, (float, type(None)))


class TestRepositoryIntegration:
    """Test repository interactions."""

    def test_repository_data_flow(self):
        """Test data flow between repositories."""
        # Create repositories
        stock_repo = InMemoryStockRepository()
        query_repo = InMemoryQueryResultRepository()

        # Create application service
        service = QueryProcessingApplicationService(
            stock_repo=stock_repo,
            recommendation_repo=InMemoryAnalystRecommendationRepository(),
            news_repo=InMemoryCompanyNewsRepository(),
            query_result_repo=query_repo
        )

        # Setup and process
        stock = Stock(StockSymbol("TEST"), current_price=Price(Decimal("100.00")))
        stock_repo.save(stock)

        result = service.process_query("Price of TEST")

        # Verify data flows correctly
        assert result.success
        assert len(query_repo.find_recent(10)) == 1

        # Verify stock data retrieval
        retrieved_stock = stock_repo.find_by_symbol(StockSymbol("TEST"))
        assert retrieved_stock.current_price.value == Decimal("100.00")


# Note: Bootstrap integration tests removed as they require external dependencies (YFinance)
# These would be tested in a full integration test suite with proper mocking
