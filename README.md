# locust-otel-generator
Locust loadtest generating otel metrics

## Environment variables
- `ENABLE_METRICS`: If enabled, will send otel counter metric (`/example-payloads/metric-counter.json`) for each (locust) user every second. Defaults to `true`.
- `ENABLE_LOGS`: If enabled, will send otel log message (`/example-payloads/logs.json`) for each (locust) user every second. Defaults to `true`.

In addition, configuring locust can be done in `locust.conf` file before running/building.

## Run locally
1. Edit locust.conf to fit your needs

2. Run locust
```
ENABLE_METRICS=true ENABLE_LOGS=true locust
```

## Run with Docker
1. Edit locust.conf to fit your needs
2. Build image:
```
docker build -t loadtest-otel-generator .
```
3. Run image:
```
docker run -p 8089:8089 -e ENABLE_METRICS=true -e ENABLE_LOGS=false loadtest-otel-generator
```