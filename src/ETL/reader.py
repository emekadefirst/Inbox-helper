import csv
import json
from collections.abc import Iterator
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any
import openpyxl


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in row.items():
        normalized_key = "_".join(str(key).strip().casefold().split())
        if isinstance(value, str):
            value = value.strip()
        normalized[normalized_key] = value
    return normalized


def read_csv(content: bytes) -> Iterator[dict[str, Any]]:
    with StringIO(content.decode("utf-8-sig"), newline="") as file:
        yield from csv.DictReader(file)

def read_xlsx(content: bytes) -> Iterator[dict[str, Any]]:
    wb = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
    try:
        rows = wb.active.iter_rows(values_only=True)
        headers = [str(h).strip() if h is not None else "" for h in next(rows, ())]
        for values in rows:
            if not any(v is not None and str(v).strip() for v in values):
                continue                                       
            yield dict(zip(headers, values))
    finally:
        wb.close()

def read_json(content: bytes) -> Iterator[dict[str, Any]]:
    data = json.loads(content.decode("utf-8"))
    if isinstance(data, dict):
        data = data.get("applications", [data])
    yield from data

READERS = {".csv": read_csv, ".xlsx": read_xlsx, ".json": read_json}