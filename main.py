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


import tkinter as tk
from tkinter import messagebox

def get_current_date() -> datetime.date:
    now = time.localtime()
    return datetime.date(now.tm_year, now.tm_mon, now.tm_mday)


def get_selected_date(day_number: int) -> datetime.date:
    today = get_current_date()
    return today + datetime.timedelta(days=day_number - 1)


def get_available_times(selected_date: datetime.date) -> list[str]:
    matching_items = [
        item for item in data.get("list", [])
        if item_date(item) == selected_date
    ]
    return sorted({parse_item_datetime(item).time().strftime("%H:%M") for item in matching_items})


def get_forecasts_for_date_time(selected_date: datetime.date, selected_time: str) -> list[dict]:
    return [
        item for item in data.get("list", [])
        if item_date(item) == selected_date and parse_item_datetime(item).time().strftime("%H:%M") == selected_time
    ]


def clear_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()


def show_weather_details(selected_date: datetime.date, selected_time: str) -> None:
    forecasts = get_forecasts_for_date_time(selected_date, selected_time)
    clear_frame(button_frame)
    title_label.config(text=f"Weather for {selected_date} at {selected_time}")

    if not forecasts:
        details_label.config(text="No forecast available for that time.")
        back_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        return

    text_lines = []
    for item in forecasts:
        weather = item["weather"][0]
        main = item["main"]
        summary = summarize_weather(weather["main"])
        timestamp = parse_item_datetime(item)
        text_lines.extend([
            f"Date: {timestamp.date().isoformat()}",
            f"Time: {timestamp.time().strftime('%H:%M')}",
            f"Weather: {weather['main']} - {weather['description']}",
            f"Condition: {summary}",
            f"Temperature: {main['temp']} °C",
            f"Feels like: {main['feels_like']} °C",
            f"Humidity: {main['humidity']} %",
            f"Pressure: {main['pressure']} hPa",
            "",
        ])
    details_label.config(text="\n".join(text_lines).strip())
    back_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))


def show_time_buttons(day_number: int) -> None:
    selected_date = get_selected_date(day_number)
    available_times = get_available_times(selected_date)
    clear_frame(button_frame)
    title_label.config(text=f"What time weather do you want to know for {selected_date}?")

    if not available_times:
        details_label.config(text=f"No forecast entries found for day {day_number} ({selected_date}).")
        back_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        return

    details_label.config(text="")
    for index, time_option in enumerate(available_times):
        btn = tk.Button(
            button_frame,
            text=time_option,
            width=12,
            command=lambda t=time_option, d=selected_date: show_weather_details(d, t)
        )
        btn.grid(row=index // 3, column=index % 3, padx=5, pady=5)
    back_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))


def build_date_buttons() -> None:
    clear_frame(button_frame)
    title_label.config(text="Which day's weather do you want to know?")
    details_label.config(text="")
    back_button.grid_forget()

    for day_number in range(1, 6):
        selected_date = get_selected_date(day_number)
        day_label = f"Day {day_number}\n({selected_date.isoformat()})"
        btn = tk.Button(
            button_frame,
            text=day_label,
            width=16,
            height=2,
            command=lambda d=day_number: show_time_buttons(d)
        )
        btn.grid(row=(day_number - 1) // 2, column=(day_number - 1) % 2, padx=8, pady=8)


def start_gui() -> None:
    global root, title_label, button_frame, details_label, back_button

    root = tk.Tk()
    root.title("Weather Report")
    root.geometry("480x420")
    root.resizable(False, False)

    title_label = tk.Label(root, text="Which day's weather do you want to know?", font=("Arial", 14), wraplength=440)
    title_label.pack(padx=10, pady=(15, 10))

    button_frame = tk.Frame(root)
    button_frame.pack(padx=10, pady=5)

    details_label = tk.Label(root, text="", font=("Arial", 11), justify="left", anchor="w", wraplength=440)
    details_label.pack(padx=10, pady=10, fill="both")

    back_button = tk.Button(root, text="Back", width=12, command=build_date_buttons)

    build_date_buttons()
    root.mainloop()


if __name__ == "__main__":
    try:
        start_gui()
    except Exception as exc:
        messagebox.showerror("Error", f"An error occurred: {exc}")

