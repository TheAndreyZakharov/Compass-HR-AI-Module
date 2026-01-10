from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from compass_hr_ai.utils.paths import DataPaths


def _extract_courses_from_payload(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("courses"), list):
        return [x for x in data["courses"] if isinstance(x, dict)]
    if isinstance(data, dict) and isinstance(data.get("id"), int):
        return [data]
    return []


def _flatten_course(c: dict[str, Any]) -> dict[str, Any]:
    cid = c.get("id")
    return {
        "course_id": cid,
        "title": c.get("title"),
        "slug": c.get("slug"),
        "summary": c.get("summary"),
        "description": c.get("description"),
        "language": c.get("language"),
        "level": c.get("level"),
        "is_paid": c.get("is_paid"),
        "price": c.get("price"),
        "certificate": c.get("certificate"),
        "learners_count": c.get("learners_count"),
        "review_summary": c.get("review_summary"),
        "cover": c.get("cover"),
        "canonical_url": c.get("canonical_url"),
        "url": (f"https://stepik.org/course/{cid}" if cid else None),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=str, default="", help="Stepik cache dir (courses)")
    ap.add_argument("--out", type=str, default="", help="Output parquet path")
    args = ap.parse_args()

    paths = DataPaths.build()
    in_dir = Path(args.input_dir) if args.input_dir else (paths.cache / "stepik" / "courses")
    out_path = Path(args.out) if args.out else (paths.processed / "courses.parquet")

    files = sorted(in_dir.glob("*.json"))
    if not files:
        raise SystemExit(f"No json files in: {in_dir}. Run stepik_fetch first.")

    rows: list[dict[str, Any]] = []
    bad = 0

    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            bad += 1
            continue

        courses = _extract_courses_from_payload(data)
        if not courses:
            bad += 1
            continue

        for c in courses:
            rows.append(_flatten_course(c))

    if not rows:
        raise SystemExit(
            "No courses parsed from cached payloads. "
            "Send first 50 lines of one file from data/cache/stepik/courses/*.json"
        )

    df = pd.DataFrame(rows).drop_duplicates(subset=["course_id"]).sort_values("course_id")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    print(f"OK: parsed {len(df)} courses -> {out_path} (bad_files={bad})")


if __name__ == "__main__":
    main()