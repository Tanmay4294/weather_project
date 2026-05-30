import datetime

from parse_item_datetime import parse_item_datetime


def build_forecast_index(forecast_data: dict) -> tuple[dict[datetime.date, list[str]], dict[tuple[datetime.date, str], list[dict]]]:
    times_by_date = {}
    forecasts_by_date_time = {}

    for item in forecast_data.get("list", []):
        timestamp = parse_item_datetime(item)
        selected_date = timestamp.date()
        selected_time = timestamp.time().strftime("%H:%M")

        if selected_date not in times_by_date:
            times_by_date[selected_date] = set()
        times_by_date[selected_date].add(selected_time)

        key = (selected_date, selected_time)
        if key not in forecasts_by_date_time:
            forecasts_by_date_time[key] = []
        forecasts_by_date_time[key].append(item)

    sorted_times_by_date = {
        selected_date: sorted(times)
        for selected_date, times in times_by_date.items()
    }
    return sorted_times_by_date, forecasts_by_date_time
