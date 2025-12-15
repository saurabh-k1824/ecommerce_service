from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "path", "status"]
)

ERROR_COUNT = Counter(
    "api_errors_total",
    "Total number of API error responses",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency in seconds",
    ["method", "path"]
)
