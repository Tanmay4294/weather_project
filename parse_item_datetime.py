import datetime


datetime_cache = {}


def parse_item_datetime(item: dict) -> datetime.datetime:
    timestamp_text = item["dt_txt"]
    if timestamp_text not in datetime_cache:
        datetime_cache[timestamp_text] = datetime.datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
    return datetime_cache[timestamp_text]
