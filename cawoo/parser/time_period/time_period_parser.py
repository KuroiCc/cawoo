import re
from datetime import datetime

from ..interface import IParser
from cawoo.entities import TimePeriod


class TimePeriodParser(IParser):

    @classmethod
    def parse(cls, str_time_period) -> TimePeriod:
        """
        以下のような形の文字列をTimePeriodに変換する

        2022/04/19 21:00-22:00
        """
        # 出勤日時の形式チェック
        # 正しい形式: `2022/04/19 21:00-22:00`
        pattern = r'\d{4}(\/)\d{1,2}\1\d{1,2} \d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}'
        if re.match(pattern, str_time_period) is None:
            raise ValueError(f'{str_time_period} is not a valid date time format')

        date, time = str_time_period.split(' ')
        start_t, end_t = time.split('-')
        return TimePeriod(
            start=datetime.strptime(f'{date} {start_t}', '%Y/%m/%d %H:%M'),
            end=datetime.strptime(f'{date} {end_t}', '%Y/%m/%d %H:%M'),
        )
