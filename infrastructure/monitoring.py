"""Monitoring and metrics for fault tolerance and system health."""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .fault_tolerance import CircuitBreaker

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """Health status of a component."""
    component: str
    status: str  # "healthy", "degraded", "unhealthy"
    last_check: datetime
    message: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    uptime_seconds: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)


class MonitoringService:
    """Service for monitoring system health and fault tolerance."""

    def __init__(self):
        self.health_checks: Dict[str, HealthStatus] = {}
        self.system_metrics = SystemMetrics()
        self.circuit_breakers: List[CircuitBreaker] = []
        self.start_time = datetime.now()

    def register_circuit_breaker(self, circuit_breaker: CircuitBreaker):
        """Register a circuit breaker for monitoring."""
        self.circuit_breakers.append(circuit_breaker)
        logger.info(f"Registered circuit breaker for monitoring: {circuit_breaker.name}")

    def record_request(self, success: bool, response_time: float):
        """Record a request for metrics."""
        self.system_metrics.total_requests += 1
        if success:
            self.system_metrics.successful_requests += 1
        else:
            self.system_metrics.failed_requests += 1

        # Update average response time
        if self.system_metrics.total_requests == 1:
            self.system_metrics.average_response_time = response_time
        else:
            self.system_metrics.average_response_time = (
                (self.system_metrics.average_response_time * (self.system_metrics.total_requests - 1)) +
                response_time
            ) / self.system_metrics.total_requests

    def update_health_status(self, component: str, status: str, message: str = "", metrics: Dict[str, Any] = None):
        """Update health status of a component."""
        self.health_checks[component] = HealthStatus(
            component=component,
            status=status,
            last_check=datetime.now(),
            message=message,
            metrics=metrics or {}
        )

        if status == "unhealthy":
            logger.warning(f"Component {component} is unhealthy: {message}")
        elif status == "degraded":
            logger.info(f"Component {component} is degraded: {message}")

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        component_statuses = [h.status for h in self.health_checks.values()]

        # Determine overall status
        if "unhealthy" in component_statuses:
            overall_status = "unhealthy"
        elif "degraded" in component_statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"

        # Calculate uptime
        uptime = datetime.now() - self.start_time

        # Get circuit breaker metrics
        circuit_metrics = {}
        for cb in self.circuit_breakers:
            circuit_metrics[cb.name] = cb.get_metrics()

        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime.total_seconds(),
            "components": {
                name: {
                    "status": health.status,
                    "last_check": health.last_check.isoformat(),
                    "message": health.message,
                    "metrics": health.metrics
                }
                for name, health in self.health_checks.items()
            },
            "system_metrics": {
                "total_requests": self.system_metrics.total_requests,
                "successful_requests": self.system_metrics.successful_requests,
                "failed_requests": self.system_metrics.failed_requests,
                "success_rate": (
                    self.system_metrics.successful_requests /
                    max(1, self.system_metrics.total_requests)
                ),
                "average_response_time": self.system_metrics.average_response_time
            },
            "circuit_breakers": circuit_metrics
        }

    def check_circuit_breaker_health(self):
        """Check health of all registered circuit breakers."""
        for cb in self.circuit_breakers:
            metrics = cb.get_metrics()

            if cb.state.value == "open":
                status = "unhealthy"
                message = f"Circuit breaker is OPEN - API unavailable"
            elif cb.state.value == "half_open":
                status = "degraded"
                message = f"Circuit breaker is testing recovery"
            else:
                # Check success rate
                success_rate = metrics.get("success_rate", 0)
                if success_rate < 0.8:  # Less than 80% success rate
                    status = "degraded"
                    message = ".1%"
                else:
                    status = "healthy"
                    message = ".1%"

            self.update_health_status(
                f"circuit_breaker_{cb.name}",
                status,
                message,
                metrics
            )

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get current alerts based on health status."""
        alerts = []

        # Check unhealthy components
        for component, health in self.health_checks.items():
            if health.status == "unhealthy":
                alerts.append({
                    "level": "critical",
                    "component": component,
                    "message": health.message,
                    "timestamp": health.last_check.isoformat()
                })
            elif health.status == "degraded":
                alerts.append({
                    "level": "warning",
                    "component": component,
                    "message": health.message,
                    "timestamp": health.last_check.isoformat()
                })

        # Check circuit breaker alerts
        for cb in self.circuit_breakers:
            if cb.state.value == "open":
                alerts.append({
                    "level": "critical",
                    "component": f"circuit_breaker_{cb.name}",
                    "message": f"Circuit breaker is OPEN - API calls blocked",
                    "timestamp": datetime.now().isoformat()
                })
            elif cb.state.value == "half_open":
                alerts.append({
                    "level": "warning",
                    "component": f"circuit_breaker_{cb.name}",
                    "message": f"Circuit breaker is testing recovery",
                    "timestamp": datetime.now().isoformat()
                })

        # Check low success rate
        success_rate = (
            self.system_metrics.successful_requests /
            max(1, self.system_metrics.total_requests)
        )
        if success_rate < 0.9 and self.system_metrics.total_requests > 10:
            alerts.append({
                "level": "warning",
                "component": "system",
                "message": ".1%",
                "timestamp": datetime.now().isoformat()
            })

        return alerts


# Global monitoring instance
monitoring_service = MonitoringService()


def get_monitoring_service() -> MonitoringService:
    """Get the global monitoring service instance."""
    return monitoring_service
