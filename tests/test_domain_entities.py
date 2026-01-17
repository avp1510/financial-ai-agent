"""Unit tests for domain entities."""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from domain.entities import (
    StockSymbol, Price, MarketCap, Stock, Recommendation,
    AnalystRecommendation, CompanyNews, Query, QueryResult
)


class TestValueObjects:
    """Test value objects."""

    def test_stock_symbol_creation(self):
        """Test StockSymbol creation and validation."""
        # Valid symbol
        symbol = StockSymbol("AAPL")
        assert symbol.symbol == "AAPL"
        assert symbol.normalized == "AAPL"

        # Test normalization
        symbol_upper = StockSymbol("aapl")
        assert symbol_upper.normalized == "AAPL"

    def test_stock_symbol_validation(self):
        """Test StockSymbol validation."""
        # Empty symbol should fail
        with pytest.raises(ValueError, match="Stock symbol cannot be empty"):
            StockSymbol("")

        # Too long symbol should fail
        with pytest.raises(ValueError, match="Stock symbol too long"):
            StockSymbol("A" * 11)

    def test_price_creation(self):
        """Test Price value object."""
        price = Price(value=Decimal("150.50"), currency="USD")
        assert price.value == Decimal("150.50")
        assert price.currency == "USD"
        assert price.formatted() == "$150.50"

    def test_price_validation(self):
        """Test Price validation."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Price(value=Decimal("-10.00"))

    def test_market_cap_creation(self):
        """Test MarketCap value object."""
        # Billion
        cap_billion = MarketCap(value=Decimal("5000000000"))
        assert cap_billion.formatted() == "$5.0B"

        # Trillion
        cap_trillion = MarketCap(value=Decimal("2000000000000"))
        assert "T" in cap_trillion.formatted()

    def test_market_cap_validation(self):
        """Test MarketCap validation."""
        with pytest.raises(ValueError, match="Market cap cannot be negative"):
            MarketCap(value=Decimal("-1000000"))


class TestEntities:
    """Test domain entities."""

    def test_stock_creation(self):
        """Test Stock entity creation."""
        symbol = StockSymbol("AAPL")
        price = Price(value=Decimal("150.00"))
        market_cap = MarketCap(value=Decimal("2500000000000"))

        stock = Stock(
            symbol=symbol,
            name="Apple Inc.",
            current_price=price,
            market_cap=market_cap,
            sector="Technology",
            pe_ratio=Decimal("28.5")
        )

        assert stock.symbol.symbol == "AAPL"
        assert stock.name == "Apple Inc."
        assert stock.current_price.value == Decimal("150.00")
        assert stock.sector == "Technology"
        assert stock.pe_ratio == Decimal("28.5")
        assert stock.is_technology_stock()

    def test_stock_price_update(self):
        """Test updating stock price."""
        symbol = StockSymbol("AAPL")
        stock = Stock(symbol=symbol)

        new_price = Price(value=Decimal("155.00"))
        stock.update_price(new_price)

        assert stock.current_price.value == Decimal("155.00")
        assert stock.last_updated is not None

    def test_analyst_recommendation_creation(self):
        """Test AnalystRecommendation entity."""
        symbol = StockSymbol("AAPL")
        price_target = Price(value=Decimal("180.00"))

        rec = AnalystRecommendation(
            symbol=symbol,
            firm="Goldman Sachs",
            recommendation=Recommendation.BUY,
            price_target=price_target
        )

        assert rec.symbol.symbol == "AAPL"
        assert rec.firm == "Goldman Sachs"
        assert rec.recommendation == Recommendation.BUY
        assert rec.is_bullish()
        assert not rec.is_bearish()
        assert rec.price_target.value == Decimal("180.00")

    def test_company_news_creation(self):
        """Test CompanyNews entity."""
        symbol = StockSymbol("AAPL")
        published_date = datetime.now() - timedelta(days=5)  # 5 days ago

        news = CompanyNews(
            symbol=symbol,
            title="Apple Reports Strong Q4 Earnings",
            summary="Apple exceeded expectations with $25B revenue",
            source="Bloomberg",
            url="https://bloomberg.com/apple-earnings",
            published_date=published_date,
            sentiment="positive"
        )

        assert news.symbol.symbol == "AAPL"
        assert news.title == "Apple Reports Strong Q4 Earnings"
        assert news.source == "Bloomberg"
        assert news.is_recent(30)  # Should be recent within 30 days
        assert news.sentiment == "positive"

    def test_query_creation_and_analysis(self):
        """Test Query entity."""
        query = Query(content="What is the current price of AAPL?")

        # Test symbol extraction would be handled by domain service
        # but we can test the entity structure
        assert query.content == "What is the current price of AAPL?"
        assert query.query_type == "general"  # default
        assert query.symbols == []

        # Test adding symbols
        symbol = StockSymbol("AAPL")
        query.add_symbol(symbol)
        assert len(query.symbols) == 1
        assert query.symbols[0].symbol == "AAPL"
        assert query.is_multi_symbol_query() is False

    def test_query_result_creation(self):
        """Test QueryResult entity."""
        query = Query(content="Test query")
        result = QueryResult(
            query=query,
            response="Test response",
            sources=["Source 1", "Source 2"],
            processing_time=1.5,
            success=True
        )

        assert result.query.content == "Test query"
        assert result.response == "Test response"
        assert len(result.sources) == 2
        assert result.processing_time == 1.5
        assert result.success is True

        # Test adding sources
        result.add_source("Source 3")
        assert len(result.sources) == 3

    def test_query_result_error_handling(self):
        """Test QueryResult error handling."""
        query = Query(content="Failed query")
        result = QueryResult(query=query, response="", success=False, error_message="API Error")

        result.mark_failed("Network timeout")
        assert result.success is False
        assert result.error_message == "Network timeout"


class TestRecommendationEnum:
    """Test Recommendation enum."""

    def test_recommendation_values(self):
        """Test all recommendation values."""
        assert Recommendation.STRONG_BUY.value == "Strong Buy"
        assert Recommendation.BUY.value == "Buy"
        assert Recommendation.HOLD.value == "Hold"
        assert Recommendation.SELL.value == "Sell"
        assert Recommendation.STRONG_SELL.value == "Strong Sell"
