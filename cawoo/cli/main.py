from pathlib import Path

import typer

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
):
    """
    notionからの勤怠表を集計する\n
    ! いかなる場合において休憩時間は通常勤務時間としてカウントする
    """
    typer.echo(f'{src}')


if __name__ == "__main__":
    cli_app()
