# Monitoring System with Prometheus + Grafana (PostgreSQL + Node Exporter + Weather API)

Adapted version of the original monitoring project, modified to use **PostgreSQL** instead of SQLite
and a **WeatherAPI-based custom exporter** instead of the original example.

## Components

- PostgreSQL with Olist demo data (customers + orders)
- Postgres Exporter (prometheuscommunity/postgres-exporter)
- Node Exporter (system / container metrics)
- Custom Exporter (`custom_exporter.py`) that pulls current weather from WeatherAPI
- Prometheus
- Grafana with **3 dashboards**:
  - `postgres_dashboard.json` – DB exporter dashboard
  - `node_dashboard.json` – Node exporter dashboard
  - `weather_dashboard.json` – Weather custom exporter dashboard

## How to run

1. Create a file `.env` in this folder (optional) and export:

   ```bash
   export WEATHER_API_KEY=YOUR_KEY_HERE
   export WEATHER_CITY="Astana"
   ```

   Or on Windows PowerShell:

   ```powershell
   $env:WEATHER_API_KEY="YOUR_KEY_HERE"
   $env:WEATHER_CITY="Astana"
   ```

2. Start the stack:

   ```bash
   docker-compose up -d --build
   ```

3. Open:

   - Prometheus: http://localhost:9090
   - Grafana:    http://localhost:3000  (login: admin / admin)
   - Node Exporter: http://localhost:9100/metrics
   - Weather Exporter: http://localhost:8000/metrics
   - Postgres Exporter: http://localhost:9187/metrics

4. In Grafana you will see 3 provisioned dashboards in the **Monitoring** folder.
