"""Bootstrap configuration for the Financial AI Agent system using DDD."""

import logging
from typing import Optional
from application.services import (
    FinancialAnalysisService, QueryProcessingApplicationService, AnalyticsService
)
from domain.repositories import (
    StockRepository, AnalystRecommendationRepository, CompanyNewsRepository, QueryResultRepository,
    InMemoryQueryResultRepository
)
from infrastructure.yfinance_adapter import (
    YFinanceStockRepository, YFinanceAnalystRecommendationRepository, YFinanceCompanyNewsRepository
)
from infrastructure.monitoring import get_monitoring_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ApplicationContext:
    """Application context that manages dependency injection and service initialization."""

    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self._services = {}

        # Initialize repositories
        self._initialize_repositories()

        # Initialize application services
        self._initialize_services()

        # Register circuit breakers with monitoring
        self._register_monitoring()

        logger.info("Application context initialized successfully")

    def _initialize_repositories(self):
        """Initialize all repository implementations."""
        # Stock data repositories
        self._services['stock_repository'] = YFinanceStockRepository(
            cache_duration_minutes=15 if self.use_cache else 0
        )
        self._services['analyst_repository'] = YFinanceAnalystRecommendationRepository(
            cache_duration_minutes=60 if self.use_cache else 0
        )
        self._services['news_repository'] = YFinanceCompanyNewsRepository(
            cache_duration_minutes=30 if self.use_cache else 0
        )

        # Query result repository (in-memory for now)
        self._services['query_result_repository'] = InMemoryQueryResultRepository()

    def _initialize_services(self):
        """Initialize application services with their dependencies."""
        # Financial Analysis Service
        self._services['financial_analysis_service'] = FinancialAnalysisService(
            stock_repo=self._services['stock_repository'],
            recommendation_repo=self._services['analyst_repository'],
            news_repo=self._services['news_repository'],
            query_result_repo=self._services['query_result_repository']
        )

        # Query Processing Service
        self._services['query_processing_service'] = QueryProcessingApplicationService(
            stock_repo=self._services['stock_repository'],
            recommendation_repo=self._services['analyst_repository'],
            news_repo=self._services['news_repository'],
            query_result_repo=self._services['query_result_repository']
        )

        # Analytics Service
        self._services['analytics_service'] = AnalyticsService(
            query_result_repo=self._services['query_result_repository']
        )

    def _register_monitoring(self):
        """Register circuit breakers and components with monitoring service."""
        monitoring = get_monitoring_service()

        # Register circuit breakers from repositories
        stock_repo = self._services['stock_repository']
        if hasattr(stock_repo, 'circuit_breaker'):
            monitoring.register_circuit_breaker(stock_repo.circuit_breaker)

        recommendation_repo = self._services['analyst_repository']
        if hasattr(recommendation_repo, 'circuit_breaker'):
            monitoring.register_circuit_breaker(recommendation_repo.circuit_breaker)

        # Initialize health status
        monitoring.update_health_status("stock_repository", "healthy", "Initialized")
        monitoring.update_health_status("recommendation_repository", "healthy", "Initialized")
        monitoring.update_health_status("query_processing_service", "healthy", "Initialized")

    # Service accessors
    @property
    def financial_analysis_service(self) -> FinancialAnalysisService:
        return self._services['financial_analysis_service']

    @property
    def query_processing_service(self) -> QueryProcessingApplicationService:
        return self._services['query_processing_service']

    @property
    def analytics_service(self) -> AnalyticsService:
        return self._services['analytics_service']

    # Repository accessors (for testing or direct access if needed)
    @property
    def stock_repository(self) -> StockRepository:
        return self._services['stock_repository']

    @property
    def analyst_repository(self) -> AnalystRecommendationRepository:
        return self._services['analyst_repository']

    @property
    def news_repository(self) -> CompanyNewsRepository:
        return self._services['news_repository']

    @property
    def query_result_repository(self) -> QueryResultRepository:
        return self._services['query_result_repository']


# Global application context
_app_context: Optional[ApplicationContext] = None


def get_application_context() -> ApplicationContext:
    """Get the global application context, creating it if necessary."""
    global _app_context
    if _app_context is None:
        _app_context = ApplicationContext()
    return _app_context


def create_test_context() -> ApplicationContext:
    """Create a test context with no caching."""
    return ApplicationContext(use_cache=False)


# Convenience functions for easy access
def get_query_processor() -> QueryProcessingApplicationService:
    """Get the query processing service."""
    return get_application_context().query_processing_service


def get_financial_analyzer() -> FinancialAnalysisService:
    """Get the financial analysis service."""
    return get_application_context().financial_analysis_service


def get_analytics() -> AnalyticsService:
    """Get the analytics service."""
    return get_application_context().analytics_service
