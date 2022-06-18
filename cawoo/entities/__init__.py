from datetime import datetime, timedelta, date
from typing import Optional

from pydantic import BaseModel

from .selector import Selector, SelectableBaseModel


class TimePeriod(BaseModel):
    start: datetime
    end: datetime


class WorkPeriod(BaseModel):
    working_period: TimePeriod
    rest_time: timedelta


class AttendanceRaw(SelectableBaseModel, WorkPeriod):
    pass


class WorkHour(BaseModel):
    date: date
    working_period: list[WorkPeriod]
    rest_time: timedelta
    operating_hours: timedelta
    overtime_period: Optional[list[TimePeriod]]
    overtime_hours: Optional[timedelta]
    late_night_period: Optional[list[TimePeriod]]
    late_night_hours: Optional[timedelta]


class Attendance(SelectableBaseModel, WorkHour):
    pass


class Result(BaseModel):
    err: list[str] = []
    res: Optional[Selector[Attendance]]
    attendance_raw: Selector[AttendanceRaw]

    def __init__(self, *, err=[], res=[], attendance_raw):
        super().__init__(
            err=err,
            res=Selector[Attendance](res),
            attendance_raw=Selector[AttendanceRaw](attendance_raw)
        )

    class Config:
        arbitrary_types_allowed = True
