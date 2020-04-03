import datetime
import pytz


def get_now_utc():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
