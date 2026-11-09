from abc import ABC, abstractmethod


class CsvFormatError(ValueError):
    """Нарушен формат CSV-строки (наследник ValueError)."""


class ICsvRowParser(ABC):
    @abstractmethod
    def parse_row(self, line, delimiter=","):
        """Разбирает одну строку CSV и возвращает list[str]."""

    @abstractmethod
    def to_csv_row(self, fields):
        """Собирает строку CSV из list[str] и возвращает str."""
