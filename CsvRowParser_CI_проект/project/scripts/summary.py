"""Сводка по JUnit-отчётам pytest в формате Markdown.

Использование:
    python scripts/summary.py results.xml        # один отчёт
    python scripts/summary.py results/           # все results.xml в папке (по одному на ветку)
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def read(path):
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    total = int(suite.get("tests", 0))
    failed = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
    skipped = int(suite.get("skipped", 0))
    seconds = float(suite.get("time", 0))
    bad = [c.get("name") for c in suite.iter("testcase")
           if c.find("failure") is not None or c.find("error") is not None]
    return total, total - failed - skipped, failed, seconds, bad


def main(arg):
    p = Path(arg)
    files = sorted(p.rglob("results.xml")) if p.is_dir() else [p]
    print("| Источник | Статус | Всего | Пройдено | Упало | Время, с |")
    print("|---|---|---|---|---|---|")
    details = []
    for f in files:
        name = f.parent.name.replace("junit-", "") if p.is_dir() else f.name
        total, ok, failed, sec, bad = read(f)
        print(f"| {name} | {'✅' if failed == 0 else '❌'} | {total} | {ok} | {failed} | {sec:.2f} |")
        if bad:
            details.append(f"- **{name}**: " + ", ".join(sorted(bad)))
    if details:
        print("\nУпавшие тесты:\n")
        print("\n".join(details))


if __name__ == "__main__":
    main(sys.argv[1])
