import datetime
import importlib
import os
import tkinter as tk
from tkinter import messagebox

from clear_frame import clear_frame
from get_available_times import get_available_times
from get_forecasts_for_date_time import get_forecasts_for_date_time
from get_selected_date import get_selected_date
from parse_item_datetime import parse_item_datetime
from summarize_weather import summarize_weather


def show_weather_details(selected_date: datetime.date, selected_time: str) -> None:
    global details_window_id, button_frame_window_id
    forecasts = get_forecasts_for_date_time(selected_date, selected_time)
    clear_frame(button_frame)
    title_label.config(text=f"Weather for {selected_date} at {selected_time}")

    if button_frame_window_id is not None:
        canvas.delete(button_frame_window_id)
        button_frame_window_id = None

    if not forecasts:
        details_label.config(text="No forecast available for that time.")
        if details_window_id is None:
            details_window_id = canvas.create_window(canvas_width // 2, 270, window=details_label, width=720, height=180, anchor="n")
        back_button.place(relx=0.5, y=470, anchor="center")
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
            f"Temperature: {main['temp']} Â°C",
            f"Feels like: {main['feels_like']} Â°C",
            f"Humidity: {main['humidity']} %",
            f"Pressure: {main['pressure']} hPa",
            "",
        ])
    details_label.config(text="\n".join(text_lines).strip())
    if details_window_id is None:
        details_window_id = canvas.create_window(canvas_width // 2, 270, window=details_label, width=720, height=180, anchor="n")
    back_button.place(relx=0.5, y=470, anchor="center")


def show_time_buttons(day_number: int) -> None:
    global details_window_id, button_frame_window_id
    selected_date = get_selected_date(day_number)
    available_times = get_available_times(selected_date)
    clear_frame(button_frame)
    title_label.config(text=f"What time weather do you want to know for {selected_date}?")

    if not available_times:
        details_label.config(text=f"No forecast entries found for day {day_number} ({selected_date}).")
        if details_window_id is None:
            details_window_id = canvas.create_window(canvas_width // 2, 270, window=details_label, width=720, height=180, anchor="n")
        back_button.place(relx=0.5, y=470, anchor="center")
        return

    details_label.config(text="")
    if details_window_id is not None:
        canvas.delete(details_window_id)
        details_window_id = None
    if button_frame_window_id is None:
        button_frame_window_id = canvas.create_window(canvas_width // 2, 160, window=button_frame, anchor="n")
    for index, time_option in enumerate(available_times):
        btn = tk.Button(
            button_frame,
            text=time_option,
            width=12,
            bg="#e8f0ff",
            fg="#082145",
            relief="raised",
            bd=2,
            command=lambda t=time_option, d=selected_date: show_weather_details(d, t)
        )
        btn.grid(row=index // 3, column=index % 3, padx=5, pady=5)
    back_button.place(relx=0.5, y=400, anchor="center")


def build_date_buttons() -> None:
    global details_window_id, button_frame_window_id
    clear_frame(button_frame)
    title_label.config(text="Which day's weather do you want to know?")
    details_label.config(text="")
    if details_window_id is not None:
        canvas.delete(details_window_id)
        details_window_id = None
    if button_frame_window_id is None:
        button_frame_window_id = canvas.create_window(canvas_width // 2, 160, window=button_frame, anchor="n")
    back_button.place_forget()

    for day_number in range(1, 6):
        selected_date = get_selected_date(day_number)
        day_label = f"Day {day_number}\n({selected_date.isoformat()})"
        btn = tk.Button(
            button_frame,
            text=day_label,
            width=14,
            height=2,
            command=lambda d=day_number: show_time_buttons(d),
            bg="#d9e6ff",
            fg="#081b33",
            relief="raised",
            bd=2
        )
        btn.grid(row=(day_number - 1) // 3, column=(day_number - 1) % 3, padx=6, pady=6)


def start_gui() -> None:
    global root, title_label, button_frame, details_label, back_button, canvas, canvas_width, canvas_height, details_window_id, button_frame_window_id
    details_window_id = None
    button_frame_window_id = None

    root = tk.Tk()
    root.title("Weather Report")
    root.resizable(False, False)

    canvas_width = 750
    canvas_height = 520
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    bg_image = None
    bg_path = "background.png"
    if os.path.exists(bg_path):
        try:
            Image = importlib.import_module("PIL.Image")
            ImageTk = importlib.import_module("PIL.ImageTk")
            pil_image = Image.open(bg_path).resize((canvas_width, canvas_height), Image.ANTIALIAS)
            bg_image = ImageTk.PhotoImage(pil_image)
        except (ImportError, ModuleNotFoundError, Exception):
            if bg_path.lower().endswith(".png"):
                try:
                    photo = tk.PhotoImage(file=bg_path)
                    img_w = photo.width()
                    img_h = photo.height()
                    if img_w != canvas_width or img_h != canvas_height:
                        subsample_x = max(1, img_w // canvas_width)
                        subsample_y = max(1, img_h // canvas_height)
                        photo = photo.subsample(subsample_x, subsample_y)
                    bg_image = photo
                except tk.TclError:
                    bg_image = None

    if bg_image:
        canvas_width = bg_image.width()
        canvas_height = bg_image.height()
        root.geometry(f"{canvas_width}x{canvas_height}")
        canvas.config(width=canvas_width, height=canvas_height)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        root.bg_image = bg_image
    else:
        root.geometry(f"{canvas_width}x{canvas_height}")
        canvas.configure(bg="#5f7ea0")

    title_label = tk.Label(root, text="Which day's weather do you want to know?", font=("Arial", 15, "bold"), wraplength=500, justify="center", bg="#ffffff", fg="#212121")
    button_frame = tk.Frame(root, bg="#ffffff")
    details_label = tk.Label(root, text="", font=("Arial", 11), justify="center", anchor="center", wraplength=500, bg="#f4f4f4", fg="#101010", relief="groove", bd=2)
    back_button = tk.Button(root, text="Back", width=14, command=build_date_buttons, bg="#4a86e8", fg="#ffffff")

    canvas.create_window(canvas_width // 2, 25, window=title_label, anchor="n")

    build_date_buttons()
    root.mainloop()


if __name__ == "__main__":
    try:
        start_gui()
    except Exception as exc:
        messagebox.showerror("Error", f"An error occurred: {exc}")
