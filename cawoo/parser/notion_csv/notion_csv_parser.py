import csv
import re
from pathlib import Path
from datetime import timedelta

from ..interface import IParser
from ..time_period import TimePeriodParser
from ...entities import Result, AttendanceRaw
from ...utils import get_work_date
from ...config import settings


class NotionCsvParser(IParser):

    @classmethod
    def parse(cls, file_path: Path) -> Result:
        attendance_key = '予実'
        attended_key = '実績'
        work_hour_key = '出勤日時'
        rest_time_key = '休憩時間（分）'
        people = '人'

        res: list[AttendanceRaw] = []
        err_lines: list[str] = []
        with file_path.open('r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    # スペース変換　全角 -> 半角
                    row[people] = re.sub('\s', ' ', row[people])
                    # 実績のみ抽出
                    if row[attendance_key] != attended_key:
                        raise ValueError('not attended')
                    # 出勤日時形式変換　str -> TimePeriod
                    time_period = cls._parse_time_period(row[work_hour_key])
                    res.append(AttendanceRaw(  # yapf: disable
                        date=get_work_date(time_period, settings.OPENING_TIME),
                        people=row[people],
                        working_period=time_period,
                        rest_time=timedelta(
                            minutes=int(row[rest_time_key]) if (row[rest_time_key] != '') else 0
                        ),
                    ))
                except Exception as e:
                    err_lines.append(str({'err': str(e), 'line': row}))

        return Result(attendance_raw=res, err=err_lines)

    @staticmethod
    def _parse_time_period(str_time_period):
        return TimePeriodParser.parse(str_time_period)
