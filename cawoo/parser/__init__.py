from enum import Enum

from .notion_csv import NotionCsvParser


class ParserType(Enum):
    NOTION_CSV_PARSER = 'notion_csv'


parsers = {
    ParserType.NOTION_CSV_PARSER: NotionCsvParser,
}
