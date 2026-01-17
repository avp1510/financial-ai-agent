"""Application services that orchestrate domain services for use cases."""

import logging
import time
from typing import List, Optional
from domain.entities import Stock, StockSymbol, Query, QueryResult
from domain.services import (
    QueryProcessingService, QueryAnalysisService,
    RecommendationAnalysisService, NewsAnalysisService
)
from domain.repositories import (
    StockRepository, AnalystRecommendationRepository,
    CompanyNewsRepository, QueryResultRepository
)
from infrastructure.monitoring import get_monitoring_service

logger = logging.getLogger(__name__)


class FinancialAnalysisService:
    """Application service for financial analysis operations."""

    def __init__(self,
                 stock_repo: StockRepository,
                 recommendation_repo: AnalystRecommendationRepository,
                 news_repo: CompanyNewsRepository,
                 query_result_repo: QueryResultRepository):
        self.stock_repo = stock_repo
        self.recommendation_repo = recommendation_repo
        self.news_repo = news_repo
        self.query_result_repo = query_result_repo

    def get_stock_analysis(self, symbol: StockSymbol) -> Optional[dict]:
        """Get comprehensive analysis for a stock."""
        try:
            stock = self.stock_repo.find_by_symbol(symbol)
            if not stock:
                return None

            recommendations = self.recommendation_repo.find_recent_by_symbol(symbol, limit=20)
            news = self.news_repo.find_recent_by_symbol(symbol, limit=10)

            # Analyze recommendations
            rec_analyzer = RecommendationAnalysisService()
            rec_analysis = rec_analyzer.analyze_recommendations(recommendations)

            # Analyze news sentiment
            news_analyzer = NewsAnalysisService()
            news_sentiment = news_analyzer.analyze_sentiment(news)

            return {
                "stock": stock,
                "recommendations": recommendations,
                "recommendation_analysis": rec_analysis,
                "news": news,
                "news_sentiment": news_sentiment
            }

        except Exception as e:
            logger.error(f"Error analyzing stock {symbol.symbol}: {e}")
            return None


class QueryProcessingApplicationService:
    """Application service for processing user queries."""

    def __init__(self,
                 stock_repo: StockRepository,
                 recommendation_repo: AnalystRecommendationRepository,
                 news_repo: CompanyNewsRepository,
                 query_result_repo: QueryResultRepository):
        self.stock_repo = stock_repo
        self.recommendation_repo = recommendation_repo
        self.news_repo = news_repo
        self.query_result_repo = query_result_repo

        # Initialize domain services
        self.query_analyzer = QueryAnalysisService()
        self.rec_analyzer = RecommendationAnalysisService()
        self.news_analyzer = NewsAnalysisService()

        # Create the query processing service
        self.query_processor = QueryProcessingService(
            stock_service=self,  # This service implements StockDataService protocol
            query_analyzer=self.query_analyzer,
            recommendation_analyzer=self.rec_analyzer,
            news_analyzer=self.news_analyzer
        )

    def process_query(self, query_text: str) -> QueryResult:
        """Process a user query and return results."""
        logger.info(f"Processing query: {query_text}")
        monitoring = get_monitoring_service()
        start_time = time.time()

        try:
            result = self.query_processor.process_query(query_text)

            # Save the result for analytics/caching
            self.query_result_repo.save(result)

            # Record metrics
            processing_time = result.processing_time or (time.time() - start_time)
            monitoring.record_request(result.success, processing_time)

            # Update health status
            if result.success:
                monitoring.update_health_status(
                    "query_processing_service",
                    "healthy",
                    f"Query processed successfully in {processing_time:.2f}s"
                )
            else:
                monitoring.update_health_status(
                    "query_processing_service",
                    "degraded",
                    f"Query failed: {result.error_message}"
                )

            logger.info(f"Query processed successfully in {processing_time:.2f}s")
            return result

        except Exception as e:
            logger.error(f"Error processing query '{query_text}': {e}")

            # Record failed request
            processing_time = time.time() - start_time
            monitoring.record_request(False, processing_time)
            monitoring.update_health_status(
                "query_processing_service",
                "unhealthy",
                f"Query processing failed: {str(e)}"
            )

            error_result = QueryResult(
                query=Query(content=query_text),
                response="",
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
            return error_result

    # Implement StockDataService protocol methods
    def get_stock_info(self, symbol: StockSymbol) -> Optional[Stock]:
        """Get comprehensive stock information."""
        return self.stock_repo.find_by_symbol(symbol)

    def get_stock_price(self, symbol: StockSymbol) -> Optional[float]:
        """Get current stock price."""
        stock = self.stock_repo.find_by_symbol(symbol)
        return float(stock.current_price.value) if stock and stock.current_price else None

    def get_analyst_recommendations(self, symbol: StockSymbol) -> List:
        """Get analyst recommendations for a stock."""
        return self.recommendation_repo.find_recent_by_symbol(symbol, limit=20)

    def get_company_news(self, symbol: StockSymbol, limit: int = 10) -> List:
        """Get recent company news."""
        return self.news_repo.find_recent_by_symbol(symbol, limit=limit)


class AnalyticsService:
    """Application service for analytics and reporting."""

    def __init__(self, query_result_repo: QueryResultRepository):
        self.query_result_repo = query_result_repo

    def get_query_statistics(self) -> dict:
        """Get statistics about query processing."""
        recent_results = self.query_result_repo.find_recent(limit=1000)

        total_queries = len(recent_results)
        successful_queries = sum(1 for r in recent_results if r.success)
        failed_queries = total_queries - successful_queries

        avg_processing_time = sum(r.processing_time or 0 for r in recent_results if r.processing_time) / max(1, len([r for r in recent_results if r.processing_time]))

        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "failed_queries": failed_queries,
            "success_rate": successful_queries / max(1, total_queries),
            "average_processing_time": avg_processing_time
        }

    def get_popular_symbols(self, limit: int = 10) -> List[tuple]:
        """Get most queried stock symbols."""
        recent_results = self.query_result_repo.find_recent(limit=500)

        symbol_counts = {}
        for result in recent_results:
            for symbol in result.query.symbols:
                symbol_counts[symbol.symbol] = symbol_counts.get(symbol.symbol, 0) + 1

        return sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
