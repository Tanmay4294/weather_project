import datetime
import requests
import time

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
    raise SystemExit


def summarize_weather(weather_main: str) -> str:
    condition = weather_main.lower()
    if condition in {"clear", "sunny"}:
        return "Sunny"
    if condition in {"rain", "rainy", "drizzle", "thunderstorm"}:
        return "Rainy"
    if condition in {"clouds", "cloudy"}:
        return "Cloudy"
    if condition in {"mist", "haze", "fog", "smoke"}:
        return "Hazy"
    if condition in {"snow", "sleet"}:
        return "Snowy"
    return weather_main.capitalize()


def parse_item_datetime(item: dict) -> datetime.datetime:
    return datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")


def item_date(item: dict) -> datetime.date:
    return parse_item_datetime(item).date()


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
    print(f"  Temperature: {main['temp']} °C")
    print(f"  Feels like: {main['feels_like']} °C")
    print(f"  Humidity: {main['humidity']} %")
    print(f"  Pressure: {main['pressure']} hPa")
    print()


def get_day_choice() -> int:
    while True:
        choice = input("Enter a day number 1-5 (1=today, 2=tomorrow, 3=day after tomorrow): ").strip()
        if choice.isdigit():
            day_number = int(choice)
            if 1 <= day_number <= 5:
                return day_number
        print("Invalid selection. Please enter a number from 1 to 5.")


def get_selected_date(day_number: int) -> datetime.date:
    now = time.localtime()
    today = datetime.date(now.tm_year, now.tm_mon, now.tm_mday)
    return today + datetime.timedelta(days=day_number - 1)


def choose_time_for_date(available_times: list[str], date_text: str) -> str:
    print(f"Available times for {date_text}:")
    for t in available_times:
        print(f"  - {t}")
    while True:
        user_time = input("Enter the time you want to know (HH:MM): ").strip()
        if user_time in available_times:
            return user_time
        print("Wrong time. Please enter one of the available times exactly as shown.")


day_choice = get_day_choice()
selected_date = get_selected_date(day_choice)
selected_day_items = [
    item for item in data.get("list", [])
    if item_date(item) == selected_date
]

if selected_day_items:
    available_times = sorted({parse_item_datetime(item).time().strftime("%H:%M") for item in selected_day_items})
    selected_time = choose_time_for_date(available_times, selected_date.isoformat())
    print(f"Weather for day {day_choice} ({selected_date}) at {selected_time}:")
    for item in selected_day_items:
        if parse_item_datetime(item).time().strftime("%H:%M") == selected_time:
            print_forecast(item)
else:
    print(f"No forecast entries found for day {day_choice} ({selected_date}).")

