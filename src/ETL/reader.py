import csv, json
from collections.abc import Iterator
from pathlib import Path
from typing import Any
import openpyxl

def read_csv(path: str) -> Iterator[dict[str, Any]]:
    with open(path, newline="", encoding="utf-8-sig") as f:   
        yield from csv.DictReader(f)

def read_xlsx(path: str) -> Iterator[dict[str, Any]]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        rows = wb.active.iter_rows(values_only=True)
        headers = [str(h).strip() if h is not None else "" for h in next(rows, ())]
        for values in rows:
            if not any(v is not None and str(v).strip() for v in values):
                continue                                       
            yield dict(zip(headers, values))
    finally:
        wb.close()

def read_json(path: str) -> Iterator[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("applications", [data])
    yield from data

READERS = {".csv": read_csv, ".xlsx": read_xlsx, ".json": read_json}