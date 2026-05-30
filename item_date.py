import datetime

from parse_item_datetime import parse_item_datetime


def item_date(item: dict) -> datetime.date:
    return parse_item_datetime(item).date()
