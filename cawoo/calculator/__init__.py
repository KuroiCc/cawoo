from datetime import datetime, timedelta

from ..entities import Result, AttendanceRaw, WorkHour, TimePeriod, WorkPeriod, Attendance, Selector
from ..config import settings


def calculate_work_hours(raw_list: list[AttendanceRaw]) -> WorkHour:
    """
    `list[AttendanceRaw]` から一人一日の勤務時間を計算する
    """
    raw_list.sort(key=lambda x: x.working_period.start)
    total_rest_time = timedelta()

    working_period: list[WorkPeriod] = []
    operating_hours = timedelta()
    overtime_period: list[TimePeriod] = []
    overtime_hours = timedelta()
    late_night_period: list[TimePeriod] = []
    late_night_hours = timedelta()

    for record in raw_list:
        operating_hour = record.working_period.end - record.working_period.start - record.rest_time
        working_period.append(WorkPeriod(**record.dict()))
        operating_hours += operating_hour
        total_rest_time += record.rest_time

        # 残業時間
        if operating_hours <= timedelta(hours=settings.WORKING_HOURS):
            # 仕事時間8時間以下の場合
            pass
        elif overtime_hours == timedelta():
            # 境目の場合
            first_overtime_period = TimePeriod(
                start=record.working_period.end -
                (operating_hours - timedelta(hours=settings.WORKING_HOURS)),
                end=record.working_period.end,
            )
            overtime_period.append(first_overtime_period)
            overtime_hours += first_overtime_period.end - first_overtime_period.start
        else:
            overtime_period.append(record.working_period)
            overtime_hours += operating_hour

        # 深夜時間
        if record.working_period.end.time() <= settings.LATE_NIGHT_TIME:
            # 終了時間が22時以上の場合
            pass
        elif record.working_period.start.time() < settings.LATE_NIGHT_TIME:
            # 境目の場合
            first_late_night_period = TimePeriod(
                start=datetime.combine(
                    record.working_period.start.date(),
                    settings.LATE_NIGHT_TIME,
                ),
                end=record.working_period.end,
            )
            late_night_period.append(first_late_night_period)
            late_night_hours += first_late_night_period.end - first_late_night_period.start
        else:
            late_night_period.append(record.working_period)
            late_night_hours += operating_hour

    return WorkHour(
        date=raw_list[0].working_period.start.date(),
        working_period=working_period,
        rest_time=total_rest_time,
        operating_hours=operating_hours,
        overtime_period=overtime_period,
        overtime_hours=overtime_hours,
        late_night_period=late_night_period,
        late_night_hours=late_night_hours,
    )


def analyze(parse_result: Result):
    group_by_people = parse_result.attendance_raw._group_by_people
    group_by_date = parse_result.attendance_raw._group_by_date

    res = Selector[Attendance]([])
    for people in group_by_people:
        for dt in group_by_date:
            group_by_date_people = list(set(group_by_date[dt]) & set(group_by_people[people]))
            if not group_by_date_people:
                continue
            res.append(
                Attendance(
                    people=people,
                    **calculate_work_hours(group_by_date_people).dict(),
                )
            )

    parse_result.res = res

    return parse_result
