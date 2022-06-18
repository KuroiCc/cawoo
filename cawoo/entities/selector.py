from __future__ import annotations
from datetime import datetime, date
from typing import TYPE_CHECKING, TypeVar, Generic, List, overload

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import TimePeriod


class SelectableBaseModel(BaseModel):
    """
    `BaseModel`は`set()`されることができるように
    `__eq__`と`__hash__`を実装している。
    """
    date: date
    people: str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.json() == other.json()

    def __hash__(self):
        return hash(self.json())


year = month = day = int
T = TypeVar('T', bound=BaseModel)
DateGroup = dict[year, dict[month, dict[day, list[T]]]]
SelectableType = TypeVar('SelectableType', bound=SelectableBaseModel)


class Selector(Generic[SelectableType]):

    def __init__(self, list: list[SelectableType]):
        self._list: List[SelectableType] = []
        self._group_by_people: dict[str, List[SelectableType]] = {}
        self._group_by_date: dict[datetime, List[SelectableType]] = {}
        # self._group_by_day: DateGroup[SelectableType] = {}
        for attendance in list:
            self.append(attendance)

    def __getitem__(self, key):
        return self._list[key]

    def __setitem__(self, key, value):
        self._list[key] = value

    def append(self, item: SelectableType):
        # ? ここでitemの型をチェックする方法ある？
        self._list.append(item)

        if item.people not in self._group_by_people:
            self._group_by_people[item.people] = []
        self._group_by_people[item.people].append(item)

        if item.date not in self._group_by_date:
            self._group_by_date[item.date] = []
        self._group_by_date[item.date].append(item)

        # dt = item.date
        # if dt.year not in self._group_by_day:
        #     self._group_by_day[dt.year] = {}
        # if dt.month not in self._group_by_day[dt.year]:
        #     self._group_by_day[dt.year][dt.month] = {}
        # if dt.day not in self._group_by_day[dt.year][dt.month]:
        #     self._group_by_day[dt.year][dt.month][dt.day] = []
        # self.group_by_day[dt.year][dt.month][dt.day].append(item)

    @overload
    def get(self, *, people: str) -> List[SelectableType]:
        return self._group_by_people[people]

    @overload
    def get(self, *, date: date) -> List[SelectableType]:
        ...

    @overload
    def get(self, *, people: str, date: date) -> List[SelectableType]:
        ...

    @overload
    def get(self, *, time_period: TimePeriod) -> List[SelectableType]:
        ...

    @overload
    def get(self, *, people: str, time_period: TimePeriod) -> List[SelectableType]:
        ...

    def get(self, *, people: str = None, date: date = None, time_period: TimePeriod = None):
        if people is not None:
            if date is not None:
                # people, date
                return list(set(self._group_by_date[date]) & set(self._group_by_people[people]))
            elif time_period is not None:
                # people, time_period
                return list(
                    set(self._group_by_people[people])
                    & set(self._get_by_time_period(time_period=time_period))  # noqa: W503
                )
            else:
                # people
                return self._group_by_people[people]
        elif date is not None:
            # date
            return self._group_by_date[date]
        elif time_period is not None:
            # time_period
            return self._get_by_time_period(time_period=time_period)
        else:
            # all None
            return self._list

    def _get_by_time_period(self, *, time_period: TimePeriod) -> List[SelectableType]:
        return [
            item for item in self._list
            if time_period.start.date() <= item.date <= time_period.end.date()
        ]
