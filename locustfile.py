from locust import HttpUser, TaskSet, task, constant_throughput
import json, os

headers = {"Content-Type": "application/json"}

class GeneratorBehavior(TaskSet):
    def on_start(self):
      self.env_enable_logs = os.getenv("ENABLE_LOGS", "false").lower() == "true"
      self.env_enable_metrics = os.getenv("ENABLE_METRICS", "false").lower() == "true"
      self.env_print_status_code = os.getenv("PRINT_STATUS_CODE", "false").lower() == "true"
      self.env_logs_payload = os.getenv("LOGS_PAYLOAD", None)
      self.env_metric_payload = os.getenv("METRIC_PAYLOAD", None)
      print("Sending telemetry to endpoint: ", self.client.base_url)

    @task(1)
    def send_telemetry(self):
      # Logs
      if self.env_enable_logs:
        if self.env_logs_payload is None:
          with open("example-payloads/logs.json") as f:
            logs_payload = json.load(f)
          response = self.client.post("/v1/logs", json=logs_payload, headers=headers)
        else:
          response = self.client.post("/v1/logs", json=self.env_logs_payload, headers=headers)
        if self.env_print_status_code:
          print("Response status code:", response.status_code)

      # Metrics
      if self.env_enable_metrics:
        if self.env_metric_payload is None:
          with open("example-payloads/metric-counter.json") as f:
            metric_payload = json.load(f)
          response = self.client.post("/v1/metrics", json=metric_payload, headers=headers)
        else:
          response = self.client.post("/v1/metrics", json=self.env_metric_payload, headers=headers)
        if self.env_print_status_code:
          print("Response status code:", response.status_code)

class OtelUser(HttpUser):
    tasks = [GeneratorBehavior]
    wait_time = constant_throughput(1)
