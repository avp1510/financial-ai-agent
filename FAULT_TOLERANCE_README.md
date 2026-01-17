# Fault Tolerance Implementation

## Overview

The Financial AI Agent implements comprehensive fault tolerance patterns to ensure reliable operation even when external APIs are unavailable or experiencing issues. The system uses Circuit Breakers, Retry Mechanisms, and Fallback Handlers to provide resilience.

## Fault Tolerance Patterns

### 1. Circuit Breaker Pattern

**Purpose**: Prevents cascading failures by stopping calls to failing services.

**Implementation**: `infrastructure/fault_tolerance.py:CircuitBreaker`

**Configuration**:
- **Failure Threshold**: 3-5 consecutive failures
- **Recovery Timeout**: 30-60 seconds
- **Success Threshold**: 3 successes needed to close circuit in half-open state

**States**:
- **Closed**: Normal operation, calls pass through
- **Open**: Failing service, calls rejected immediately
- **Half-Open**: Testing recovery, limited calls allowed

### 2. Retry Mechanism

**Purpose**: Handle transient failures with exponential backoff.

**Implementation**: `infrastructure/fault_tolerance.py:RetryMechanism`

**Configuration**:
- **Max Attempts**: 2-3 retries
- **Initial Delay**: 1.0 seconds
- **Backoff Factor**: 2.0 (exponential)
- **Max Delay**: 60 seconds
- **Jitter**: ±25% random variation

### 3. Fallback Handler

**Purpose**: Provide graceful degradation when primary services fail.

**Implementation**: `infrastructure/fault_tolerance.py:FallbackHandler`

**Features**:
- **Cache-based Fallbacks**: Use previously successful responses
- **TTL-based Expiration**: Configurable cache lifetimes (10-30 minutes)
- **Default Responses**: Return basic data structures when all else fails

### 4. Monitoring and Alerting

**Purpose**: Track system health and provide operational visibility.

**Implementation**: `infrastructure/monitoring.py:MonitoringService`

**Metrics Tracked**:
- Request success/failure rates
- Response times
- Circuit breaker states
- Component health status
- Alert generation for issues

## Integration Points

### YFinance Adapter

```python
# Circuit breaker for stock data API
self.circuit_breaker = CircuitBreaker(
    "yfinance_stock_api",
    CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0)
)

# Retry mechanism for transient failures
self.retry_mechanism = RetryMechanism(
    RetryConfig(max_attempts=2, initial_delay=1.0)
)

# Fallback handler with caching
self.fallback_handler = FallbackHandler(
    FallbackConfig(enabled=True, cache_ttl=600)
)
```

### Application Services

```python
# Request monitoring
monitoring.record_request(result.success, processing_time)

# Health status updates
monitoring.update_health_status(
    "query_processing_service",
    "healthy" if result.success else "degraded",
    f"Query processed in {processing_time:.2f}s"
)
```

## Error Scenarios Handled

### 1. API Rate Limiting
- Circuit breaker prevents overwhelming failing APIs
- Retry with backoff handles temporary rate limits
- Fallback provides cached data

### 2. Network Failures
- Retry mechanism handles intermittent connectivity
- Circuit breaker prevents cascade during outages
- Fallback ensures basic functionality

### 3. API Service Outages
- Circuit breaker opens quickly to prevent resource waste
- Monitoring alerts operators to service issues
- Fallback provides degraded but functional service

### 4. Data Parsing Errors
- Individual record failures don't break entire responses
- Logging captures parsing issues for debugging
- Fallback ensures partial data availability

## Monitoring Dashboard

Access system health via monitoring service:

```python
from infrastructure.monitoring import get_monitoring_service

monitoring = get_monitoring_service()
health_status = monitoring.get_system_health()
alerts = monitoring.get_alerts()
```

Health status includes:
- Overall system status (healthy/degraded/unhealthy)
- Component-level health
- Circuit breaker states
- Success rates and response times
- Active alerts

## Configuration Tuning

### Circuit Breaker Tuning

```python
# Aggressive - Quick failure detection
CircuitBreakerConfig(
    failure_threshold=2,      # Fail fast
    recovery_timeout=15.0     # Quick recovery attempts
)

# Conservative - Allow more failures
CircuitBreakerConfig(
    failure_threshold=10,     # More tolerant
    recovery_timeout=120.0    # Longer recovery time
)
```

### Retry Strategy Tuning

```python
# Aggressive retries
RetryConfig(
    max_attempts=5,           # More attempts
    initial_delay=0.5,        # Faster initial retry
    backoff_factor=1.5        # Slower backoff growth
)

# Conservative retries
RetryConfig(
    max_attempts=1,           # Minimal retries
    initial_delay=5.0,        # Slower initial retry
)
```

## Testing Fault Tolerance

Run fault tolerance tests:

```bash
# Test circuit breaker behavior
pytest tests/ -k "fault_tolerance"

# Test with simulated failures
pytest tests/ -k "resilience"

# Integration tests with fault injection
pytest tests/test_integration.py::TestFaultTolerance
```

## Operational Procedures

### Investigating Alerts

1. Check monitoring dashboard for failing components
2. Review circuit breaker states - OPEN indicates service issues
3. Check external API status pages
4. Review application logs for detailed error messages

### Manual Circuit Breaker Control

```python
# Force circuit breaker state (for testing/maintenance)
circuit_breaker.state = CircuitBreakerState.CLOSED  # Force close
circuit_breaker.state = CircuitBreakerState.OPEN    # Force open
```

### Cache Management

```python
# Clear fallback caches during maintenance
fallback_handler.cache.clear()

# Adjust cache TTL for different environments
FallbackConfig(cache_ttl=300)  # 5 minutes for development
FallbackConfig(cache_ttl=3600) # 1 hour for production
```

## Performance Impact

- **Circuit Breaker**: Minimal overhead when closed, fast rejection when open
- **Retry**: Additional latency only during failures, exponential backoff prevents thundering herd
- **Fallback**: Fast cache lookups, minimal impact on normal operations
- **Monitoring**: Lightweight metrics collection with configurable sampling

## Future Enhancements

- **Bulkhead Pattern**: Isolate different API calls to prevent single failure affecting all
- **Adaptive Circuit Breakers**: Dynamic thresholds based on time-of-day or load
- **Service Mesh Integration**: Distributed fault tolerance across multiple instances
- **Machine Learning**: Predictive failure detection and automatic recovery
