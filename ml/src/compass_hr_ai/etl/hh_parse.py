from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from compass_hr_ai.utils.paths import DataPaths


def _flatten_item(it: dict[str, Any]) -> dict[str, Any]:
    salary = it.get("salary") or {}
    area = it.get("area") or {}
    employer = it.get("employer") or {}
    snippet = it.get("snippet") or {}
    experience = it.get("experience") or {}
    schedule = it.get("schedule") or {}
    employment = it.get("employment") or {}

    return {
        "vacancy_id": it.get("id"),
        "name": it.get("name"),
        "area_id": area.get("id"),
        "area_name": area.get("name"),
        "salary_from": salary.get("from"),
        "salary_to": salary.get("to"),
        "salary_currency": salary.get("currency"),
        "employer_id": employer.get("id"),
        "employer_name": employer.get("name"),
        "experience": experience.get("name"),
        "schedule": schedule.get("name"),
        "employment": employment.get("name"),
        "requirement": snippet.get("requirement"),
        "responsibility": snippet.get("responsibility"),
        "published_at": it.get("published_at"),
        "alternate_url": it.get("alternate_url"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=str, default="", help="HH cache dir (vacancies)")
    ap.add_argument("--out", type=str, default="", help="Output parquet path")
    args = ap.parse_args()

    paths = DataPaths.build()
    in_dir = Path(args.input_dir) if args.input_dir else (paths.cache / "hh" / "vacancies")
    out_path = Path(args.out) if args.out else (paths.processed / "hh_vacancies.parquet")

    if not in_dir.exists():
        raise SystemExit(f"input dir not found: {in_dir}")

    rows: list[dict[str, Any]] = []
    files = sorted(in_dir.glob("*.json"))
    if not files:
        raise SystemExit(f"No json files in: {in_dir}. Run hh_fetch first.")

    for fp in files:
        data = json.loads(fp.read_text(encoding="utf-8"))
        for it in data.get("items", []) or []:
            rows.append(_flatten_item(it))

    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    print(f"OK: parsed {len(df)} vacancies -> {out_path}")


if __name__ == "__main__":
    main()