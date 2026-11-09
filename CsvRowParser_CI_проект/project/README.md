# CsvRowParser: автоматизация тестирования (GitHub Actions)

Модуль `CsvRowParser` (вариант 7, ЛР1) в трёх реализациях, сгенерированных разными ИИ-системами:

| Ветка | ИИ-система |
|---|---|
| `ai-version-1` | ManusAI |
| `ai-version-2` | Deepseek |
| `ai-version-3` | Qwen |

В каждой ветке в `src/csv_row_parser.py` лежит своя реализация, тесты (`tests/`) во всех ветках одинаковые.

## Локальный запуск

    pip install -r requirements.txt
    pytest -v

## Workflow

- `.github/workflows/ci.yml` - тесты при push, pull request и вручную (workflow_dispatch);
- `.github/workflows/compare.yml` - сравнение трёх веток в одном запуске (только вручную).
