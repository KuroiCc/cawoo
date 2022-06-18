from datetime import datetime, timedelta, date
from typing import Optional

from pydantic import BaseModel


class SettableBaseModel(BaseModel):
    """
    `BaseModel`は`set()`されることができるように
    `__eq__`と`__hash__`を実装している。
    """

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.json() == other.json()

    def __hash__(self):
        return hash(self.json())


class TimePeriod(BaseModel):
    start: datetime
    end: datetime


class WorkPeriod(BaseModel):
    working_period: TimePeriod
    rest_time: timedelta


class AttendanceRaw(WorkPeriod, SettableBaseModel):
    people: str


class WorkHour(BaseModel):
    date: date
    working_period: list[WorkPeriod]
    rest_time: timedelta
    operating_hours: timedelta
    overtime_period: Optional[list[TimePeriod]]
    overtime_hours: Optional[timedelta]
    late_night_period: Optional[list[TimePeriod]]
    late_night_hours: Optional[timedelta]


class Attendance(WorkHour, SettableBaseModel):
    people: str
