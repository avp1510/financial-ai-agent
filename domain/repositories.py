"""Repository interfaces and implementations for data access."""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from .entities import Stock, StockSymbol, AnalystRecommendation, CompanyNews, QueryResult


class StockRepository(Protocol):
    """Repository interface for stock data."""

    def find_by_symbol(self, symbol: StockSymbol) -> Optional[Stock]:
        """Find a stock by its symbol."""
        ...

    def save(self, stock: Stock) -> None:
        """Save a stock entity."""
        ...

    def find_all_by_symbols(self, symbols: List[StockSymbol]) -> List[Stock]:
        """Find multiple stocks by their symbols."""
        ...


class AnalystRecommendationRepository(Protocol):
    """Repository interface for analyst recommendations."""

    def find_by_symbol(self, symbol: StockSymbol) -> List[AnalystRecommendation]:
        """Find all recommendations for a stock symbol."""
        ...

    def save_all(self, recommendations: List[AnalystRecommendation]) -> None:
        """Save multiple recommendations."""
        ...

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[AnalystRecommendation]:
        """Find recent recommendations for a symbol."""
        ...


class CompanyNewsRepository(Protocol):
    """Repository interface for company news."""

    def find_by_symbol(self, symbol: StockSymbol) -> List[CompanyNews]:
        """Find all news for a stock symbol."""
        ...

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[CompanyNews]:
        """Find recent news for a symbol."""
        ...

    def save_all(self, news: List[CompanyNews]) -> None:
        """Save multiple news items."""
        ...


class QueryResultRepository(Protocol):
    """Repository interface for query results."""

    def save(self, result: QueryResult) -> None:
        """Save a query result."""
        ...

    def find_recent(self, limit: int = 10) -> List[QueryResult]:
        """Find recent query results."""
        ...

    def find_by_query_content(self, content: str) -> Optional[QueryResult]:
        """Find a result by query content (for caching)."""
        ...


# Repository implementations would go here in the infrastructure layer
# For now, we'll create in-memory implementations for testing

class InMemoryStockRepository:
    """In-memory implementation of StockRepository for testing."""

    def __init__(self):
        self._stocks: dict[str, Stock] = {}

    def find_by_symbol(self, symbol: StockSymbol) -> Optional[Stock]:
        return self._stocks.get(symbol.normalized)

    def save(self, stock: Stock) -> None:
        self._stocks[stock.symbol.normalized] = stock

    def find_all_by_symbols(self, symbols: List[StockSymbol]) -> List[Stock]:
        result = []
        for symbol in symbols:
            stock = self.find_by_symbol(symbol)
            if stock:
                result.append(stock)
        return result


class InMemoryAnalystRecommendationRepository:
    """In-memory implementation for testing."""

    def __init__(self):
        self._recommendations: dict[str, List[AnalystRecommendation]] = {}

    def find_by_symbol(self, symbol: StockSymbol) -> List[AnalystRecommendation]:
        return self._recommendations.get(symbol.normalized, [])

    def save_all(self, recommendations: List[AnalystRecommendation]) -> None:
        for rec in recommendations:
            symbol_key = rec.symbol.normalized
            if symbol_key not in self._recommendations:
                self._recommendations[symbol_key] = []
            self._recommendations[symbol_key].append(rec)

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[AnalystRecommendation]:
        recommendations = self.find_by_symbol(symbol)
        return sorted(recommendations, key=lambda x: x.date, reverse=True)[:limit]


class InMemoryCompanyNewsRepository:
    """In-memory implementation for testing."""

    def __init__(self):
        self._news: dict[str, List[CompanyNews]] = {}

    def find_by_symbol(self, symbol: StockSymbol) -> List[CompanyNews]:
        return self._news.get(symbol.normalized, [])

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[CompanyNews]:
        news = self.find_by_symbol(symbol)
        return sorted(news, key=lambda x: x.published_date, reverse=True)[:limit]

    def save_all(self, news: List[CompanyNews]) -> None:
        for item in news:
            symbol_key = item.symbol.normalized
            if symbol_key not in self._news:
                self._news[symbol_key] = []
            self._news[symbol_key].append(item)


class InMemoryQueryResultRepository:
    """In-memory implementation for testing."""

    def __init__(self):
        self._results: List[QueryResult] = []

    def save(self, result: QueryResult) -> None:
        self._results.append(result)

    def find_recent(self, limit: int = 10) -> List[QueryResult]:
        return sorted(self._results, key=lambda x: x.generated_at, reverse=True)[:limit]

    def find_by_query_content(self, content: str) -> Optional[QueryResult]:
        for result in self._results:
            if result.query.content == content:
                return result
        return None
