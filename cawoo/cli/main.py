from datetime import datetime, timedelta
from typing import Tuple
from pathlib import Path

import typer

from ..parser import parsers, ParserType
from ..entities import TimePeriod, Selector, Attendance
from ..config import settings
from ..calculator import analyze

cli_app = typer.Typer(add_completion=False)


@cli_app.command(context_settings={'help_option_names': ['-h', '--help']})
def main(
    src: Path = typer.Argument(
        ...,
        help='Path of source file',
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    src_type: ParserType = typer.Option(
        'notion_csv',
        '--src-type',
        '-t',
        help='Specify the type of SRC (現在はnotion_csvのみ対応)',
    ),
    people: str = typer.Option(
        None,
        '--people',
        '-p',
        help='Specify the name of people',
    ),
    date_filter: Tuple[datetime, datetime] = typer.Option(
        None,
        '--date-filter',
        '-d',
        help='Specify the date range \n\n usage: -d 2020-01-01 2020-01-31',
        formats=['%Y-%m-%d'],
    ),
    opening_time: datetime = typer.Option(
        None,
        '--opening-time',
        help='Set opening time',
        formats=['%H:%M'],
    ),
    # notion_api_key: str = typer.Option(
    #     None,
    #     '--notion-api-key',
    #     help='Set Notion API key',
    # )
):
    """
    notionからの勤怠表を集計する\n
    ! いかなる場合において休憩時間は通常勤務時間としてカウントする
    """

    if opening_time:
        settings.OPENING_TIME = opening_time.time()
    # TODO: 将来notionのAPIからのデータ取得も考える（可能なら）
    # if notion_api_key:
    #     settings.NOTION_API_KEY = notion_api_key

    try:
        parser = parsers[src_type]
    except ValueError as e:
        typer.echo(e, err=True)
        raise typer.Exit(code=1)

    if date_filter:
        if date_filter[0] > date_filter[1]:
            typer.echo('start time must be earlier than end time', err=True)
            raise typer.Exit(code=1)

        date_filter = TimePeriod(start=date_filter[0], end=date_filter[1])

    # パース、集計
    res = analyze(parser.parse(src))
    # フィルタ
    res.res: Selector[Attendance] = res.res.get(people=people, time_period=date_filter)

    # errと状態が予定の出勤を出力
    for people, work_hours in res.res._group_by_people.items():
        typer.echo(
            f'==={typer.style(f" {people} ", bg=typer.colors.BLUE)}=================================='
        )
        total_operating_hours = timedelta()
        total_overtime_hours = timedelta()
        total_late_night_hours = timedelta()
        for work_hour in work_hours:
            typer.secho(f'  {work_hour.date}', fg=typer.colors.YELLOW)
            # TODO: 今は単独の休憩時間は表示できない、以降サポート
            working_period = '\n'.join(
                [
                    f'    {i.working_period.start.time()}-{i.working_period.end.time()}{f"  rest: {i.rest_time/ timedelta(minutes=1)}" if i.rest_time != timedelta(minutes=0) else ""}'
                    for i in work_hour.working_period
                ]
            )
            typer.echo(f'{working_period}')
            total_operating_hours += work_hour.operating_hours
            total_overtime_hours += work_hour.overtime_hours
            total_late_night_hours += work_hour.late_night_hours
        typer.style("勤務時間:", fg=typer.colors.GREEN)

        def get_summary_text(item_name, t: timedelta):
            return f'{typer.style(item_name, fg=typer.colors.GREEN)} {t / timedelta(minutes=1)} min ({round(t / timedelta(hours=1), 2)}h)'

        typer.echo(get_summary_text('勤務時間', total_operating_hours))
        typer.echo(get_summary_text('残業時間', total_overtime_hours))
        typer.echo(get_summary_text('深夜時間', total_late_night_hours))
    typer.echo('\n'.join(res.err))


if __name__ == "__main__":
    cli_app()
