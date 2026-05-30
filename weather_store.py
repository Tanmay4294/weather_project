import requests

from build_forecast_index import build_forecast_index
from config import API_Key, Latitude, Longitude


url = (
    "https://api.openweathermap.org/data/2.5/forecast"
    f"?lat={Latitude}&lon={Longitude}&appid={API_Key}&units=metric&lang=en"
)

response = requests.get(url)
response.raise_for_status()

data = response.json()

morning_forecasts = [
    item for item in data.get("list", [])
    if item.get("dt_txt", "").endswith("06:00:00")
]

if not morning_forecasts:
    print("No 06:00 forecast entries found in the API response.")
    raise SystemExit

TIMES_BY_DATE, FORECASTS_BY_DATE_TIME = build_forecast_index(data)
