import datetime

from weather_store import FORECASTS_BY_DATE_TIME


def get_forecasts_for_date_time(selected_date: datetime.date, selected_time: str) -> list[dict]:
    return list(FORECASTS_BY_DATE_TIME.get((selected_date, selected_time), []))
