import datetime
import time


def get_current_date() -> datetime.date:
    now = time.localtime()
    return datetime.date(now.tm_year, now.tm_mon, now.tm_mday)
