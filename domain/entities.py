"""Domain entities for the Financial AI Agent system."""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum


class Recommendation(Enum):
    """Analyst recommendation types."""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"


@dataclass(frozen=True)
class Price:
    """Value object representing a stock price."""
    value: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Price cannot be negative")

    def formatted(self) -> str:
        return f"${self.value:,.2f}"


@dataclass(frozen=True)
class MarketCap:
    """Value object representing market capitalization."""
    value: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Market cap cannot be negative")

    def formatted(self) -> str:
        if self.value >= 1_000_000_000_000:  # Trillion
            return f"${self.value / 1_000_000_000_000:.1f}T"
        elif self.value >= 1_000_000_000:  # Billion
            return f"${self.value / 1_000_000_000:.1f}B"
        elif self.value >= 1_000_000:  # Million
            return f"${self.value / 1_000_000:.1f}M"
        else:
            return f"${self.value:.0f}"


@dataclass(frozen=True)
class StockSymbol:
    """Value object representing a stock symbol/ticker."""
    symbol: str

    def __post_init__(self):
        if not self.symbol or not self.symbol.strip():
            raise ValueError("Stock symbol cannot be empty")
        if len(self.symbol) > 10:
            raise ValueError("Stock symbol too long")

    @property
    def normalized(self) -> str:
        return self.symbol.upper().strip()


@dataclass
class Stock:
    """Domain entity representing a stock."""
    symbol: StockSymbol
    name: Optional[str] = None
    current_price: Optional[Price] = None
    market_cap: Optional[MarketCap] = None
    pe_ratio: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    last_updated: datetime = field(default_factory=datetime.now)

    def update_price(self, price: Price) -> None:
        """Update the current stock price."""
        self.current_price = price
        self.last_updated = datetime.now()

    def is_technology_stock(self) -> bool:
        """Check if this is a technology stock."""
        return self.sector and "technology" in self.sector.lower()


@dataclass
class AnalystRecommendation:
    """Domain entity representing an analyst recommendation."""
    symbol: StockSymbol
    firm: str
    recommendation: Recommendation
    price_target: Optional[Price] = None
    date: datetime = field(default_factory=datetime.now)

    def is_bullish(self) -> bool:
        """Check if recommendation is bullish."""
        return self.recommendation in [Recommendation.STRONG_BUY, Recommendation.BUY]

    def is_bearish(self) -> bool:
        """Check if recommendation is bearish."""
        return self.recommendation in [Recommendation.STRONG_SELL, Recommendation.SELL]


@dataclass
class CompanyNews:
    """Domain entity representing company news."""
    symbol: StockSymbol
    title: str
    summary: Optional[str] = None
    source: str = ""
    url: Optional[str] = None
    published_date: datetime = field(default_factory=datetime.now)
    sentiment: Optional[str] = None  # positive, negative, neutral

    def is_recent(self, days: int = 7) -> bool:
        """Check if news is recent within specified days."""
        return (datetime.now() - self.published_date).days <= days


@dataclass
class Query:
    """Domain entity representing a user query."""
    content: str
    query_type: str = "general"  # general, stock_price, analyst_recommendations, news, comparison
    symbols: List[StockSymbol] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_symbol(self, symbol: StockSymbol) -> None:
        """Add a stock symbol to the query."""
        if symbol not in self.symbols:
            self.symbols.append(symbol)

    def is_multi_symbol_query(self) -> bool:
        """Check if query involves multiple symbols."""
        return len(self.symbols) > 1


@dataclass
class QueryResult:
    """Domain entity representing the result of a query."""
    query: Query
    response: str = ""
    sources: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    processing_time: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None

    def add_source(self, source: str) -> None:
        """Add a source to the result."""
        if source not in self.sources:
            self.sources.append(source)

    def mark_failed(self, error: str) -> None:
        """Mark the result as failed."""
        self.success = False
        self.error_message = error


class DomainEntity(ABC):
    """Base class for all domain entities."""

    def validate(self) -> None:
        """Validate the entity's state."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation."""
        return {}


# Type aliases for better readability
StockList = List[Stock]
RecommendationList = List[AnalystRecommendation]
NewsList = List[CompanyNews]
