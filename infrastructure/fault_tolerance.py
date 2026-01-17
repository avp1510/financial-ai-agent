"""Fault tolerance patterns for the Financial AI Agent."""

import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass, field
from functools import wraps
import random

logger = logging.getLogger(__name__)


class CircuitBreakerState(Enum):
    """States of a circuit breaker."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""
    failure_threshold: int = 5  # Number of failures before opening
    recovery_timeout: float = 60.0  # Seconds to wait before trying again
    expected_exception: tuple = (Exception,)  # Exceptions that count as failures
    success_threshold: int = 3  # Successes needed to close circuit in half-open state


@dataclass
class CircuitBreakerMetrics:
    """Metrics for circuit breaker monitoring."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None


class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance."""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitBreakerState.CLOSED
        self.metrics = CircuitBreakerMetrics()

    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply circuit breaker to a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                logger.info(f"Circuit breaker '{self.name}' entering half-open state")
            else:
                raise CircuitBreakerOpenException(f"Circuit breaker '{self.name}' is OPEN")

        try:
            self.metrics.total_calls += 1
            result = func(*args, **kwargs)

            self._record_success()
            return result

        except self.config.expected_exception as e:
            self._record_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if self.metrics.last_failure_time is None:
            return True

        return (time.time() - self.metrics.last_failure_time) >= self.config.recovery_timeout

    def _record_success(self):
        """Record a successful call."""
        self.metrics.successful_calls += 1
        self.metrics.consecutive_successes += 1
        self.metrics.consecutive_failures = 0
        self.metrics.last_success_time = time.time()

        if self.state == CircuitBreakerState.HALF_OPEN:
            if self.metrics.consecutive_successes >= self.config.success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.metrics.consecutive_successes = 0
                logger.info(f"Circuit breaker '{self.name}' closed after successful recovery")

    def _record_failure(self):
        """Record a failed call."""
        self.metrics.failed_calls += 1
        self.metrics.consecutive_failures += 1
        self.metrics.consecutive_successes = 0
        self.metrics.last_failure_time = time.time()

        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' opened due to failure in half-open state")
        elif (self.state == CircuitBreakerState.CLOSED and
              self.metrics.consecutive_failures >= self.config.failure_threshold):
            self.state = CircuitBreakerState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' opened after {self.metrics.consecutive_failures} consecutive failures")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return {
            "name": self.name,
            "state": self.state.value,
            "total_calls": self.metrics.total_calls,
            "successful_calls": self.metrics.successful_calls,
            "failed_calls": self.metrics.failed_calls,
            "success_rate": (self.metrics.successful_calls / max(1, self.metrics.total_calls)),
            "consecutive_failures": self.metrics.consecutive_failures,
            "last_failure_time": self.metrics.last_failure_time,
            "last_success_time": self.metrics.last_success_time
        }


class CircuitBreakerOpenException(Exception):
    """Exception raised when circuit breaker is open."""
    pass


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    initial_delay: float = 1.0  # Initial delay in seconds
    backoff_factor: float = 2.0  # Exponential backoff multiplier
    max_delay: float = 60.0  # Maximum delay
    jitter: bool = True  # Add random jitter to delay
    retry_on: tuple = (Exception,)  # Exceptions to retry on


class RetryMechanism:
    """Retry mechanism with exponential backoff."""

    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()

    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply retry logic to a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.execute_with_retry(func, *args, **kwargs)
        return wrapper

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.config.retry_on as e:
                last_exception = e

                if attempt < self.config.max_attempts - 1:  # Not the last attempt
                    delay = self._calculate_delay(attempt)
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay:.2f}s: {e}")
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.config.max_attempts} attempts failed for {func.__name__}: {e}")

        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for the given attempt."""
        delay = self.config.initial_delay * (self.config.backoff_factor ** attempt)
        delay = min(delay, self.config.max_delay)

        if self.config.jitter:
            # Add random jitter (±25% of delay)
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)

        return max(0, delay)


@dataclass
class FallbackConfig:
    """Configuration for fallback behavior."""
    enabled: bool = True
    cache_ttl: int = 300  # Time to live for cached fallback data (seconds)


class FallbackHandler:
    """Fallback handler for graceful degradation."""

    def __init__(self, config: FallbackConfig = None):
        self.config = config or FallbackConfig()
        self.cache: Dict[str, Dict[str, Any]] = {}

    def with_fallback(self, primary_func: Callable, fallback_func: Callable, cache_key: str = None):
        """Execute primary function with fallback."""
        def wrapper(*args, **kwargs):
            try:
                result = primary_func(*args, **kwargs)
                # Cache successful result for future fallbacks
                if cache_key and self.config.enabled:
                    self._cache_result(cache_key, result)
                return result
            except Exception as e:
                logger.warning(f"Primary function failed, attempting fallback: {e}")

                # Try cached result first
                if cache_key and self.config.enabled:
                    cached = self._get_cached_result(cache_key)
                    if cached:
                        logger.info(f"Using cached fallback data for {cache_key}")
                        return cached

                # Execute fallback function
                try:
                    fallback_result = fallback_func(*args, **kwargs)
                    # Cache fallback result
                    if cache_key and self.config.enabled:
                        self._cache_result(cache_key, fallback_result)
                    return fallback_result
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    raise fallback_error

        return wrapper

    def _cache_result(self, key: str, result: Any):
        """Cache a result with TTL."""
        self.cache[key] = {
            "data": result,
            "timestamp": time.time()
        }

    def _get_cached_result(self, key: str) -> Optional[Any]:
        """Get cached result if still valid."""
        if key not in self.cache:
            return None

        cached = self.cache[key]
        if (time.time() - cached["timestamp"]) > self.config.cache_ttl:
            del self.cache[key]
            return None

        return cached["data"]


# Global instances for easy access
default_circuit_breaker = CircuitBreaker("default_api_circuit")
default_retry = RetryMechanism()
default_fallback = FallbackHandler()


def resilient_api_call(circuit_breaker: CircuitBreaker = None,
                      retry_mechanism: RetryMechanism = None):
    """Decorator combining circuit breaker and retry for API calls."""
    cb = circuit_breaker or default_circuit_breaker
    retry = retry_mechanism or default_retry

    def decorator(func: Callable) -> Callable:
        # Apply retry first, then circuit breaker
        retried_func = retry(func)
        protected_func = cb(retried_func)
        return protected_func

    return decorator
