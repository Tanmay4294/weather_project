WEATHER_SUMMARIES = {
    "clear": "Sunny",
    "sunny": "Sunny",
    "rain": "Rainy",
    "rainy": "Rainy",
    "drizzle": "Rainy",
    "thunderstorm": "Rainy",
    "clouds": "Cloudy",
    "cloudy": "Cloudy",
    "mist": "Hazy",
    "haze": "Hazy",
    "fog": "Hazy",
    "smoke": "Hazy",
    "snow": "Snowy",
    "sleet": "Snowy",
}


def summarize_weather(weather_main: str) -> str:
    condition = weather_main.lower()
    return WEATHER_SUMMARIES.get(condition, weather_main.capitalize())
