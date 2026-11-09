from interface import ICsvRowParser, CsvFormatError


class CsvRowParser(ICsvRowParser):
    def parse_row(self, line, delimiter=","):
        if line is None:
            raise TypeError("line не может быть None")
        if len(delimiter) != 1 or delimiter in ('"', "\r", "\n"):
            raise ValueError("Недопустимый разделитель")

        fields, buf = [], []
        in_quotes = False      # мы сейчас внутри кавычек
        field_quoted = False   # поле начиналось с кавычки
        i = 0
        while i < len(line):
            c = line[i]
            if in_quotes:
                if c == '"':
                    if i + 1 < len(line) and line[i + 1] == '"':
                        buf.append('"')      # "" -> одна кавычка
                        i += 1
                    else:
                        in_quotes = False    # закрывающая кавычка
                else:
                    buf.append(c)
            elif c == delimiter:
                fields.append("".join(buf))
                buf = []
                field_quoted = False
            elif c == '"':
                if not buf and not field_quoted:
                    in_quotes = True
                    field_quoted = True
                else:
                    raise CsvFormatError("Кавычка внутри неквотированного поля")
            else:
                if field_quoted:
                    raise CsvFormatError("Текст после закрывающей кавычки")
                buf.append(c)
            i += 1

        if in_quotes:
            raise CsvFormatError("Не закрыта кавычка")
        fields.append("".join(buf))
        return fields

    def to_csv_row(self, fields):
        if fields is None:
            raise TypeError("fields не может быть None")
        return ",".join(self._escape(f) for f in fields)

    @staticmethod
    def _escape(f):
        if not f:
            return ""
        if any(ch in f for ch in (",", '"', "\r", "\n")):
            return '"' + f.replace('"', '""') + '"'
        return f
