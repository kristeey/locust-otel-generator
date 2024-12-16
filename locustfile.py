from locust import HttpUser, TaskSet, task, constant_throughput
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.metrics import get_meter
import json, os


# Construct the metric payload

# for histogram and gauges check https://github.com/open-telemetry/opentelemetry-proto/blob/35c97806f233c17680f9a00461310b17e0085dd8/examples/metrics.json
# metric_payload = {
#   "resourceMetrics": [
#     {
#       "resource": {
#         "attributes": [{"key": "service.name", "value": {"stringValue": "locust-otel-generator.service"}}]
#       },
#       "scopeMetrics": [
#         {
#           "scope": {
#             "name": "locust-otel-generator.metrics",
#             "version": "0.0.1-alpha",
#             "attributes": [{"key": "service.name", "value": {"stringValue": "locust-otel-generator.service"}}]
#           },
#           "metrics": [
#             {
#               "name": "dummy.counter",
#               "unit": "1",
#               "description": "I am a Counter",
#               "sum": {
#                 "aggregationTemporality": 1,
#                 "isMonotonic": True,
#                 "dataPoints": [
#                   {
#                     "asDouble": 5,
#                     "startTimeUnixNano": int(time.time() * 1e9),
#                     "timeUnixNano": int(time.time() * 1e9),
#                     "attributes": [{"key": "service.name","value": {"stringValue": "locust-otel-generator.service"}}]
#                   }
#                 ]
#               }
#             }
#           ]
#         }
#       ]
#     }
#   ]
# }
# C
# logs_payload = {
#   "resourceLogs": [
#     {
#       "resource": {
#         "attributes": [{"key": "service.name", "value": {"stringValue": "locust-otel-generator.service"}}]
#       },
#       "scopeLogs": [
#         {
#           "scope": {
#             "name": "locust-otel-generator.metrics",
#             "version": "0.0.1-alpha",
#             "attributes": [{"key": "service.name", "value": {"stringValue": "locust-otel-generator.service"}}]
#           },
#           "logRecords": [
#             {
#               "timeUnixNano": "1544712660300000000",
#               "observedTimeUnixNano": "1544712660300000000",
#               "severityNumber": 10,
#               "severityText": "Information",
#               "traceId": "5B8EFFF798038103D269B633813FC60C",
#               "spanId": "EEE19B7EC3C1B174",
#               "body": {
#                 "stringValue": "Example log record"
#               },
#               "attributes": [{"key": "service.name","value": {"stringValue": "locust-otel-generator.service"}}]
#             }
#           ]
#         }
#       ]
#     }
#   ]
# }

headers = {"Content-Type": "application/json"}

class GeneratorBehavior(TaskSet):
    def on_start(self):
      self.enable_logs = os.getenv("ENABLE_LOGS", "false").lower() == "true"
      self.enable_metrics = os.getenv("ENABLE_METRICS", "false").lower() == "true"

    @task(1)
    def send_telemetry(self):
      if self.enable_logs:
        with open("example-payloads/logs.json") as f:
          logs_payload = json.load(f)
        response = self.client.post("/v1/logs", json=logs_payload, headers=headers)
        print("Response status code:", response.status_code)
      if self.enable_metrics:
        with open("example-payloads/metric-counter.json") as f:
          metric_payload = json.load(f)
        response = self.client.post("/v1/metrics", json=metric_payload, headers=headers)
        print("Response status code:", response.status_code)

class OtelUser(HttpUser):
    tasks = [GeneratorBehavior]
    wait_time = constant_throughput(1)
