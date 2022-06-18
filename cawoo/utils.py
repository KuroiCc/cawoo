from datetime import time, datetime, timedelta

from .entities import TimePeriod


def get_work_date(working_period: TimePeriod, opening_time: time):
    if working_period.start >= datetime.combine(working_period.start.date(), opening_time):
        return working_period.start.date()
    else:
        return working_period.start.date() - timedelta(days=1)
