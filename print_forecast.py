from parse_item_datetime import parse_item_datetime
from summarize_weather import summarize_weather


def print_forecast(item: dict) -> None:
    timestamp = parse_item_datetime(item)
    date_text = timestamp.date().isoformat()
    time_text = timestamp.time().strftime("%H:%M")
    weather = item["weather"][0]
    main = item["main"]
    summary = summarize_weather(weather["main"])

    print(f"Date: {date_text}")
    print(f"  Time: {time_text}")
    print(f"  Weather: {weather['main']} - {weather['description']}")
    print(f"  Condition: {summary}")
    print(f"  Temperature: {main['temp']} Â°C")
    print(f"  Feels like: {main['feels_like']} Â°C")
    print(f"  Humidity: {main['humidity']} %")
    print(f"  Pressure: {main['pressure']} hPa")
    print()
