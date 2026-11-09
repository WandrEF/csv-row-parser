
from interface import ICsvRowParser


class CsvRowParser(ICsvRowParser):
    def parse_row(self, line, delimiter=","):
        if line is None:
            raise TypeError("line не может быть None")
        result, buf = [], []
        in_quotes = False
        for c in line:
            if c == '"':
                in_quotes = not in_quotes          # кавычка просто переключает режим
            elif c == delimiter and not in_quotes:
                result.append("".join(buf).strip())
                buf = []
            else:
                buf.append(c)
        if buf:                                    # пустое последнее поле теряется
            result.append("".join(buf).strip())
        return result

    def to_csv_row(self, fields):
        if fields is None:
            raise TypeError("fields не может быть None")
        parts = []
        for f in fields:
            if f is None:
                parts.append("")
            elif any(ch in f for ch in (",", '"', "\r", "\n")):
                parts.append('"' + f.replace('"', '""') + '"')
            else:
                parts.append(f)
        return ",".join(parts)
