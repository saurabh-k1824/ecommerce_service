import time
from django.utils.deprecation import MiddlewareMixin
from ecommerce_service.common.metrics import (
    REQUEST_COUNT,
    ERROR_COUNT,
    REQUEST_LATENCY,
)

class PrometheusMetricsMiddleware(MiddlewareMixin):
    """
    Collects Prometheus metrics for every HTTP request
    """

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        try:
            method = request.method
            path = request.path
            status = str(response.status_code)

            duration = time.time() - getattr(request, "_start_time", time.time())

            # Total requests
            REQUEST_COUNT.labels(
                method=method,
                path=path,
                status=status,
            ).inc()

            # Errors only
            if response.status_code >= 400:
                ERROR_COUNT.labels(
                    method=method,
                    path=path,
                    status=status,
                ).inc()

            # Latency
            REQUEST_LATENCY.labels(
                method=method,
                path=path,
            ).observe(duration)

        except Exception:
            # Metrics must NEVER break the API
            pass

        return response
