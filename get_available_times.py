import datetime

from weather_store import TIMES_BY_DATE


def get_available_times(selected_date: datetime.date) -> list[str]:
    return list(TIMES_BY_DATE.get(selected_date, []))
