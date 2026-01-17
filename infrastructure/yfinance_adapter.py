"""Infrastructure adapter for YFinance API integration."""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

from domain.entities import (
    Stock, StockSymbol, Price, MarketCap, AnalystRecommendation,
    CompanyNews, Recommendation
)
from domain.repositories import (
    StockRepository, AnalystRecommendationRepository, CompanyNewsRepository
)
from .fault_tolerance import (
    CircuitBreaker, RetryMechanism, FallbackHandler,
    resilient_api_call, CircuitBreakerConfig, RetryConfig, FallbackConfig
)

logger = logging.getLogger(__name__)


class YFinanceStockRepository(StockRepository):
    """YFinance implementation of StockRepository."""

    def __init__(self, cache_duration_minutes: int = 15):
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self._cache: Dict[str, tuple] = {}  # symbol -> (stock, timestamp)

        # Fault tolerance components
        self.circuit_breaker = CircuitBreaker(
            "yfinance_stock_api",
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0)
        )
        self.retry_mechanism = RetryMechanism(
            RetryConfig(max_attempts=2, initial_delay=1.0)
        )
        self.fallback_handler = FallbackHandler(
            FallbackConfig(enabled=True, cache_ttl=600)  # 10 minutes
        )

    def find_by_symbol(self, symbol: StockSymbol) -> Optional[Stock]:
        """Find a stock by its symbol using YFinance with fault tolerance."""
        # Check cache first (fast path)
        cached_data = self._get_cached_stock(symbol)
        if cached_data:
            return cached_data

        # Define the API call function
        def _fetch_stock_data() -> Optional[Stock]:
            ticker = yf.Ticker(symbol.symbol)
            info = ticker.info

            if not info or 'symbol' not in info:
                logger.warning(f"No data found for symbol {symbol.symbol}")
                return None

            # Create stock entity
            stock = Stock(
                symbol=symbol,
                name=info.get('longName') or info.get('shortName'),
                sector=info.get('sector'),
                industry=info.get('industry')
            )

            # Add price information
            if 'currentPrice' in info:
                stock.current_price = Price(value=info['currentPrice'])

            # Add market cap
            if 'marketCap' in info:
                stock.market_cap = MarketCap(value=info['marketCap'])

            # Add fundamentals
            if 'trailingPE' in info:
                stock.pe_ratio = info['trailingPE']

            if 'dividendYield' in info:
                stock.dividend_yield = info['dividendYield']

            return stock

        # Define fallback function
        def _fallback_stock_data() -> Optional[Stock]:
            logger.info(f"Using fallback for stock data {symbol.symbol}")
            # Return a basic stock entity with cached or default data
            return Stock(symbol=symbol, name=f"{symbol.symbol} (cached)")

        # Execute with fault tolerance
        try:
            cache_key = f"stock_{symbol.normalized}"
            stock = self.fallback_handler.with_fallback(
                lambda: self.retry_mechanism.execute_with_retry(
                    lambda: self.circuit_breaker.call(_fetch_stock_data)
                ),
                _fallback_stock_data,
                cache_key
            )

            # Cache successful result
            if stock:
                self._cache_stock(symbol, stock)

            return stock

        except Exception as e:
            logger.error(f"All fault tolerance mechanisms failed for {symbol.symbol}: {e}")
            return None

    def save(self, stock: Stock) -> None:
        """Save stock data (caching implementation)."""
        self._cache_stock(stock.symbol, stock)

    def find_all_by_symbols(self, symbols: List[StockSymbol]) -> List[Stock]:
        """Find multiple stocks by their symbols."""
        results = []
        for symbol in symbols:
            stock = self.find_by_symbol(symbol)
            if stock:
                results.append(stock)
        return results

    def _get_cached_stock(self, symbol: StockSymbol) -> Optional[Stock]:
        """Get cached stock data if still valid."""
        cached = self._cache.get(symbol.normalized)
        if cached:
            stock, timestamp = cached
            if datetime.now() - timestamp < self.cache_duration:
                return stock
            else:
                # Remove expired cache
                del self._cache[symbol.normalized]
        return None

    def _cache_stock(self, symbol: StockSymbol, stock: Stock) -> None:
        """Cache stock data with timestamp."""
        self._cache[symbol.normalized] = (stock, datetime.now())


class YFinanceAnalystRecommendationRepository(AnalystRecommendationRepository):
    """YFinance implementation of AnalystRecommendationRepository."""

    def __init__(self, cache_duration_minutes: int = 60):  # Cache longer for recommendations
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self._cache: Dict[str, tuple] = {}  # symbol -> (recommendations, timestamp)

        # Fault tolerance components
        self.circuit_breaker = CircuitBreaker(
            "yfinance_recommendations_api",
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=60.0)
        )
        self.retry_mechanism = RetryMechanism(
            RetryConfig(max_attempts=2, initial_delay=1.0)
        )
        self.fallback_handler = FallbackHandler(
            FallbackConfig(enabled=True, cache_ttl=1800)  # 30 minutes
        )

    def find_by_symbol(self, symbol: StockSymbol) -> List[AnalystRecommendation]:
        """Find all recommendations for a stock symbol with fault tolerance."""
        # Check cache first
        cached_data = self._get_cached_recommendations(symbol)
        if cached_data:
            return cached_data

        # Define the API call function
        def _fetch_recommendations() -> List[AnalystRecommendation]:
            ticker = yf.Ticker(symbol.symbol)
            recommendations_df = ticker.recommendations

            if recommendations_df is None or recommendations_df.empty:
                logger.info(f"No recommendations found for {symbol.symbol}")
                return []

            recommendations = []
            for _, row in recommendations_df.iterrows():
                try:
                    rec = AnalystRecommendation(
                        symbol=symbol,
                        firm=row.get('Firm', 'Unknown'),
                        recommendation=self._map_recommendation(row.get('To Grade', '')),
                        date=row.name if hasattr(row, 'name') else datetime.now()
                    )

                    # Add price target if available
                    if 'Price Target' in row and pd.notna(row['Price Target']):
                        rec.price_target = Price(value=row['Price Target'])

                    recommendations.append(rec)

                except Exception as e:
                    logger.warning(f"Error parsing recommendation row: {e}")
                    continue

            return recommendations

        # Define fallback function
        def _fallback_recommendations() -> List[AnalystRecommendation]:
            logger.info(f"Using fallback for recommendations {symbol.symbol}")
            # Return empty list as fallback - better than failing
            return []

        # Execute with fault tolerance
        try:
            cache_key = f"recommendations_{symbol.normalized}"
            recommendations = self.fallback_handler.with_fallback(
                lambda: self.retry_mechanism.execute_with_retry(
                    lambda: self.circuit_breaker.call(_fetch_recommendations)
                ),
                _fallback_recommendations,
                cache_key
            )

            # Cache successful results
            if recommendations is not None:
                self._cache_recommendations(symbol, recommendations)

            return recommendations or []

        except Exception as e:
            logger.error(f"All fault tolerance mechanisms failed for recommendations {symbol.symbol}: {e}")
            return []

    def save_all(self, recommendations: List[AnalystRecommendation]) -> None:
        """Save recommendations (caching implementation)."""
        if recommendations:
            symbol = recommendations[0].symbol
            self._cache_recommendations(symbol, recommendations)

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[AnalystRecommendation]:
        """Find recent recommendations for a symbol."""
        all_recommendations = self.find_by_symbol(symbol)
        return sorted(all_recommendations, key=lambda x: x.date, reverse=True)[:limit]

    def _map_recommendation(self, grade: str) -> Recommendation:
        """Map YFinance recommendation grade to our enum."""
        grade_lower = grade.lower().strip() if grade else ""

        if "strong buy" in grade_lower or "buy" == grade_lower:
            return Recommendation.STRONG_BUY
        elif "buy" in grade_lower:
            return Recommendation.BUY
        elif "hold" in grade_lower or "neutral" in grade_lower:
            return Recommendation.HOLD
        elif "sell" in grade_lower:
            return Recommendation.SELL
        elif "strong sell" in grade_lower:
            return Recommendation.STRONG_SELL
        else:
            return Recommendation.HOLD  # Default

    def _get_cached_recommendations(self, symbol: StockSymbol) -> Optional[List[AnalystRecommendation]]:
        """Get cached recommendations if still valid."""
        cached = self._cache.get(symbol.normalized)
        if cached:
            recommendations, timestamp = cached
            if datetime.now() - timestamp < self.cache_duration:
                return recommendations
            else:
                del self._cache[symbol.normalized]
        return None

    def _cache_recommendations(self, symbol: StockSymbol, recommendations: List[AnalystRecommendation]) -> None:
        """Cache recommendations with timestamp."""
        self._cache[symbol.normalized] = (recommendations, datetime.now())


class YFinanceCompanyNewsRepository(CompanyNewsRepository):
    """YFinance implementation of CompanyNewsRepository."""

    def __init__(self, cache_duration_minutes: int = 30):
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self._cache: Dict[str, tuple] = {}  # symbol -> (news, timestamp)

    def find_by_symbol(self, symbol: StockSymbol) -> List[CompanyNews]:
        """Find all news for a stock symbol."""
        try:
            # Check cache first
            cached_data = self._get_cached_news(symbol)
            if cached_data:
                return cached_data

            # Fetch from YFinance
            ticker = yf.Ticker(symbol.symbol)
            news_data = ticker.news

            if not news_data:
                logger.info(f"No news found for {symbol.symbol}")
                return []

            news_items = []
            for item in news_data[:20]:  # Limit to recent 20 items
                try:
                    news_item = CompanyNews(
                        symbol=symbol,
                        title=item.get('title', ''),
                        summary=item.get('summary', ''),
                        source=item.get('publisher', ''),
                        url=item.get('link', ''),
                        published_date=datetime.fromtimestamp(item.get('providerPublishTime', datetime.now().timestamp()))
                    )
                    news_items.append(news_item)

                except Exception as e:
                    logger.warning(f"Error parsing news item: {e}")
                    continue

            # Cache the results
            self._cache_news(symbol, news_items)

            return news_items

        except Exception as e:
            logger.error(f"Error fetching news for {symbol.symbol}: {e}")
            return []

    def find_recent_by_symbol(self, symbol: StockSymbol, limit: int = 10) -> List[CompanyNews]:
        """Find recent news for a symbol."""
        all_news = self.find_by_symbol(symbol)
        return sorted(all_news, key=lambda x: x.published_date, reverse=True)[:limit]

    def save_all(self, news: List[CompanyNews]) -> None:
        """Save news items (caching implementation)."""
        if news:
            symbol = news[0].symbol
            self._cache_news(symbol, news)

    def _get_cached_news(self, symbol: StockSymbol) -> Optional[List[CompanyNews]]:
        """Get cached news if still valid."""
        cached = self._cache.get(symbol.normalized)
        if cached:
            news, timestamp = cached
            if datetime.now() - timestamp < self.cache_duration:
                return news
            else:
                del self._cache[symbol.normalized]
        return None

    def _cache_news(self, symbol: StockSymbol, news: List[CompanyNews]) -> None:
        """Cache news with timestamp."""
        self._cache[symbol.normalized] = (news, datetime.now())
