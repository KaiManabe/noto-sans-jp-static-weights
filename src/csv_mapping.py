"""ウェイト定義 CSV を読み込む処理をまとめたモジュール"""

from __future__ import annotations

import csv
from pathlib import Path

from .models import WeightMapping


def read_weight_mappings(path: Path) -> list[WeightMapping]:
    """weight,name 列を持つ CSV からウェイト定義を読み込む"""

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = set(reader.fieldnames or ())
        missing = {"weight", "name"} - fieldnames
        if missing:
            raise ValueError(
                f"{path} must contain weight,name columns; missing: "
                f"{', '.join(sorted(missing))}"
            )

        mappings: list[WeightMapping] = []
        for line_number, row in enumerate(reader, start=2):
            raw_weight = (row.get("weight") or "").strip()
            family_name = (row.get("name") or "").strip()
            if not raw_weight and not family_name:
                continue
            if not raw_weight.isdecimal():
                raise ValueError(f"{path}:{line_number}: weight must be an integer")
            weight = int(raw_weight)
            if not 1 <= weight <= 1000:
                raise ValueError(f"{path}:{line_number}: weight must be 1..1000")
            if not family_name:
                raise ValueError(f"{path}:{line_number}: name must not be empty")
            mappings.append(WeightMapping(weight=weight, family_name=family_name))

    if not mappings:
        raise ValueError(f"{path} does not contain any weight mappings")
    return mappings
