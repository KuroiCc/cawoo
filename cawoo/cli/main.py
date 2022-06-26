from datetime import datetime
from pathlib import Path

import typer

from ..parser import parsers, ParserType
from ..entities import TimePeriod
from ..config import settings

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
    # TODO: 将来notionのAPIからのデータ取得も考える（可能なら）
    if opening_time:
        settings.OPENING_TIME = opening_time.time()
    # if notion_api_key:
    #     settings.NOTION_API_KEY = notion_api_key

    try:
        parser = parsers[src_type]
    except ValueError as e:
        typer.echo(e, err=True)
        return

    res = parser.parse(src)

    print(
        '\n'.join(
            [
                i.json() for i in sorted(
                    res.attendance_raw.get(
                        people='chin sei',
                        time_period=TimePeriod(
                            start=datetime(2022, 4, 1),
                            end=datetime(2022, 4, 18),
                        )
                    ),
                    key=lambda x: x.date
                )
            ]
        )
    )
    print('\n'.join(res.err))


if __name__ == "__main__":
    cli_app()
