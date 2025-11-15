import os
import time
import logging
from typing import Optional

import requests
from prometheus_client import Gauge, start_http_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("weather_exporter")

WEATHER_API_KEY="bd013117c36e45d6afc11921251511"
WEATHER_CITY="Astana"
WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

g_temp_c = Gauge("weather_temperature_c", "Current temperature in Celsius")
g_feelslike_c = Gauge("weather_feelslike_c", "Feels like temperature in Celsius")
g_humidity = Gauge("weather_humidity_percent", "Humidity in percent")
g_wind_kph = Gauge("weather_wind_kph", "Wind speed in kph")
g_cloud = Gauge("weather_cloud_percent", "Cloud cover in percent")
g_is_day = Gauge("weather_is_day", "Is it day (1) or night (0)")
g_last_update_ts = Gauge("weather_last_update_unix", "Last update time (unix seconds)")

def fetch_weather() -> Optional[dict]:
    if not WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY is not set! Skipping fetch.")
        return None

    params = {
        "key": WEATHER_API_KEY,
        "q": WEATHER_CITY,
        "aqi": "no",
    }
    try:
        resp = requests.get(WEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        logger.error("Failed to fetch weather data: %s", e)
        return None

def update_metrics(data: dict) -> None:
    current = data.get("current", {})
    g_temp_c.set(current.get("temp_c", 0.0))
    g_feelslike_c.set(current.get("feelslike_c", 0.0))
    g_humidity.set(current.get("humidity", 0.0))
    g_wind_kph.set(current.get("wind_kph", 0.0))
    g_cloud.set(current.get("cloud", 0.0))
    g_is_day.set(current.get("is_day", 0))
    # Prefer epoch if available, fallback to current time
    epoch = current.get("last_updated_epoch")
    if isinstance(epoch, (int, float)):
        g_last_update_ts.set(epoch)
    else:
        g_last_update_ts.set(time.time())

def main() -> None:
    logger.info("Starting WeatherAPI custom exporter on :8000")
    logger.info("City: %s", WEATHER_CITY)
    start_http_server(8000)

    while True:
        data = fetch_weather()
        if data is not None:
            update_metrics(data)
            logger.info("Updated weather metrics successfully")
        time.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    main()
