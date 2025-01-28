from prometheus_client import Counter, Histogram
import time

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

def track_metrics(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.endpoint
        response = func(*args, **kwargs)
        latency = time.time() - start_time
        REQUEST_COUNT.labels(method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(method, endpoint).observe(latency)
        return response
    return wrapper