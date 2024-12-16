# locust-otel-generator
Locust loadtest generating otel metrics

## Environment variables
- `ENABLE_METRICS`: If enabled, will send otel counter metric (`/example-payloads/metric-counter.json`) for each (locust) user every second. Defaults to `true`.
- `ENABLE_LOGS`: If enabled, will send otel log message (`/example-payloads/logs.json`) for each (locust) user every second. Defaults to `true`.

Configuring locust can be done in `locust.conf` file before running/building.

You can override the configuration in the `locust.conf` file environment variables. This is nice to know when running as docker container. The full list of environment variables can be found (here)[https://docs.locust.io/en/2.18.0/configuration.html#environment-variables], and The most common variables are:
- `LOCUST_HOST`: URL to send otel traffic to. Defaults to `https://localhost` (see `locust.conf`).
- `LOCUST_USERS`: Max number of req/sec (locust users). Defaults to `1000` (see `locust.conf`).
- `LOCUST_SPAWN_RATE`: Number of increased reqest rate per second. Defaults to `10` (see `locust.conf`).
- `LOCUST_RUN_TIME`: Run time. Defaults to `10m` (see `locust.conf`).
- `LOCUST_LOGLEVEL`: Log level DEBUG/INFO/WARNING/ERROR/CRITICAL. Defaults to `INFO` (see `locust.conf`).


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