import requests

API_Key = "e9845d6ba9d0e5920d8453e13221800c"
Latitude = 28.469709
Longitude = 77.042641

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
else:
    for item in morning_forecasts:
        date_text = item["dt_txt"].split(" ")[0]
        weather = item["weather"][0]
        main = item["main"]
        condition = weather["main"].lower()
        if condition in {"clear", "sunny"}:
            summary = "Sunny"
        elif condition in {"rain", "rainy", "drizzle", "thunderstorm"}:
            summary = "Rainy"
        elif condition in {"clouds", "cloudy"}:
            summary = "Cloudy"
        elif condition in {"mist", "haze", "fog", "smoke"}:
            summary = "Hazy"
        elif condition in {"snow", "sleet"}:
            summary = "Snowy"
        else:
            summary = weather["main"]

        print(f"Date: {date_text}")
        print(f"  Time: 06:00")
        print(f"  Weather: {weather['main']} - {weather['description']}")
        print(f"  Condition: {summary}")
        print(f"  Temperature: {main['temp']} °C")
        print(f"  Feels like: {main['feels_like']} °C")
        print(f"  Humidity: {main['humidity']} %")
        print(f"  Pressure: {main['pressure']} hPa")
        print()

