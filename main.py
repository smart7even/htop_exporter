#!/usr/bin/env python3
from prometheus_client import start_http_server, Gauge
import psutil
import time
import dotenv

dotenv.load_dotenv()

# Metrics to collect
cpu_usage_gauge = Gauge(
    'cpu_usage', 'CPU usage by process', ['process', 'pid'])
memory_usage_gauge = Gauge(
    'memory_usage', 'Memory usage by process', ['process', 'pid'])


def gather_metrics():
    """Collect metrics about CPU and memory usage."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_name = proc.info['name']
            process_pid = str(proc.info['pid'])
            process_cpu = proc.info['cpu_percent']
            process_memory = proc.info['memory_percent']

            cpu_usage_gauge.labels(process=process_name,
                                   pid=process_pid).set(process_cpu)
            memory_usage_gauge.labels(
                process=process_name, pid=process_pid).set(process_memory)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)  # Port number can be changed as needed
    print("Prometheus metrics server running on http://localhost:8000")

    # Update metrics every 10 seconds
    while True:
        gather_metrics()
        time.sleep(10)
