# CAWOO

各種形式の勤怠表を集計するCLIツール

## Help
```zsh
Usage: cawoo [OPTIONS] SRC

  notionからの勤怠表を集計する

  ! いかなる場合において休憩時間は通常勤務時間としてカウントする

Arguments:
  SRC  Path of source file  [required]

Options:
  -t, --src-type [notion_csv]     Specify the type of SRC (現在はnotion_csvのみ対応)
                                  [default: notion_csv]
  -p, --people TEXT               Specify the name of people
  -d, --date-filter <DATETIME DATETIME>...
                                  Specify the date range
                                  
                                  usage: -d 2020-01-01 2020-01-31
  --opening-time [%H:%M]          Set opening time
  -h, --help                      Show this message and exit.

```

## Usage
```zsh
cawoo ./勤怠.csv
cawoo ./勤怠.csv -p 'tanaka tarou' -d 2022-4-1 2022-4-30
```


## Install & Development
### [Poetry](https://python-poetry.org)　
**※ Recommended**
```shell
git clone https://github.com/KuroiCc/cawoo.git
cd cawoo
poetry install
# and you can run commands using poetry
poetry run cawoo -h
```
<br>

### python virtual environment
```shell
git clone https://github.com/KuroiCc/cawoo.git
cd cawoo
python -m venv env
pip install -r requirements.txt
python -m cawoo.cli -h
```