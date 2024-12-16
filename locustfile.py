from locust import HttpUser, TaskSet, task, constant_throughput
import json, os

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
        #print("Response status code:", response.status_code)
      if self.enable_metrics:
        with open("example-payloads/metric-counter.json") as f:
          metric_payload = json.load(f)
        response = self.client.post("/v1/metrics", json=metric_payload, headers=headers)
        #print("Response status code:", response.status_code)

class OtelUser(HttpUser):
    tasks = [GeneratorBehavior]
    wait_time = constant_throughput(1)
