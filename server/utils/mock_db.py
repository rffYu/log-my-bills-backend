# -*- coding: utf-8 -*-
import json
from pathlib import Path

mock_file = Path(__file__).resolve().parents[2] / "mock_data" / "mock_records.json"

def get_mock_records_json_file():
    with open(mock_file, "r", encoding="utf-8") as f:
        records = json.load(f)
    return records

