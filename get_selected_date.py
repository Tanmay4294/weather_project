import datetime

from get_current_date import get_current_date


def get_selected_date(day_number: int) -> datetime.date:
    today = get_current_date()
    return today + datetime.timedelta(days=day_number - 1)
