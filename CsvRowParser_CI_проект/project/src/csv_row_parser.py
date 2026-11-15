import re
from interface import ICsvRowParser


class CsvRowParser(ICsvRowParser):
    def parse_row(self, line, delimiter=","):
        if line is None:
            raise TypeError("line не может быть None")
        # делим по разделителю, за которым чётное число кавычек
        pattern = re.escape(delimiter) + r'(?=(?:[^"]*"[^"]*")*[^"]*$)'
        return [f.strip().strip('"') for f in re.split(pattern, line)]

    def to_csv_row(self, fields):
        if fields is None:
            raise TypeError("fields не может быть None")
        return ",".join(f'"{f}"' if "," in f else f for f in fields)
