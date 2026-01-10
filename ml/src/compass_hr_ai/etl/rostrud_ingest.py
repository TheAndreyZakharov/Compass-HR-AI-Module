from __future__ import annotations

import argparse
import re
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from compass_hr_ai.utils.paths import DataPaths

_WS_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s\-+#/]+")


def norm_title(s: str) -> str:
    s = (s or "").strip().lower()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def _detect_column(columns: Iterable[str], candidates: list[str]) -> str | None:
    cols = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    return None


def _auto_sep(path: Path) -> str:
    """
    Auto-detect separator for this dataset.
    If pandas reads only 1 column and it contains '|', treat it as '|' separated.
    """
    df0 = pd.read_csv(path, nrows=0)
    cols = list(df0.columns)
    if len(cols) == 1 and "|" in cols[0]:
        return "|"
    return ","


def inspect_csv(path: Path, sep: str) -> None:
    df = pd.read_csv(path, nrows=0, sep=sep, engine="python")
    print("CSV:", str(path))
    print("SEP:", repr(sep))
    print("COLUMNS:", list(df.columns))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workexp", type=str, default="", help="Path to dataset1.workexp.csv")
    ap.add_argument("--inspect", action="store_true", help="Print columns and exit")
    ap.add_argument("--demo-small", action="store_true", help="Process small slice for quick run")
    ap.add_argument("--chunksize", type=int, default=200_000)
    ap.add_argument("--sep", type=str, default="", help="CSV separator override (e.g. '|'). If empty => auto.")
    args = ap.parse_args()

    paths = DataPaths.build()

    workexp_path = Path(args.workexp) if args.workexp else (paths.raw / "rostrud" / "dataset1.workexp.csv")
    if not workexp_path.exists():
        raise SystemExit(f"workexp not found: {workexp_path}")

    sep = args.sep if args.sep else _auto_sep(workexp_path)

    if args.inspect:
        inspect_csv(workexp_path, sep=sep)
        return

    paths.interim.mkdir(parents=True, exist_ok=True)
    paths.processed.mkdir(parents=True, exist_ok=True)

    header = pd.read_csv(workexp_path, nrows=0, sep=sep, engine="python")
    cols = list(header.columns)

    # В твоём файле person id = id_candidate
    col_person = _detect_column(cols, ["id_candidate", "person_id", "respondent_id", "id", "ID", "pers_id", "pid"])
    col_title = _detect_column(cols, ["job_title", "position", "post", "occupation", "profession", "job", "role", "title"])
    col_start = _detect_column(cols, ["date_from", "start_date", "dt_start", "from", "start"])
    col_end = _detect_column(cols, ["date_to", "end_date", "dt_end", "to", "end"])

    if not col_person or not col_title:
        print("ERROR: cannot auto-detect required columns.")
        print("Detected:", {"person": col_person, "title": col_title, "start": col_start, "end": col_end})
        print("Run: python -m compass_hr_ai.etl.rostrud_ingest --inspect")
        raise SystemExit(2)

    usecols = [col_person, col_title]
    if col_start:
        usecols.append(col_start)
    if col_end:
        usecols.append(col_end)

    interim_clean = paths.interim / "rostrud_workexp_clean.parquet"
    if interim_clean.exists():
        interim_clean.unlink()

    rows_written = 0
    parts: list[pd.DataFrame] = []

    for chunk in pd.read_csv(
        workexp_path,
        usecols=usecols,
        chunksize=args.chunksize,
        sep=sep,
        engine="python",
    ):
        chunk = chunk.rename(
            columns={
                col_person: "person_id",
                col_title: "job_title",
                **({col_start: "start_date"} if col_start else {}),
                **({col_end: "end_date"} if col_end else {}),
            }
        )

        chunk["person_id"] = chunk["person_id"].astype(str)
        chunk["job_title_norm"] = chunk["job_title"].astype(str).map(norm_title)

        if "start_date" in chunk.columns:
            chunk["start_date"] = pd.to_datetime(chunk["start_date"], errors="coerce")
        if "end_date" in chunk.columns:
            chunk["end_date"] = pd.to_datetime(chunk["end_date"], errors="coerce")

        chunk = chunk[chunk["job_title_norm"].str.len() > 1]

        parts.append(chunk)
        rows_written += len(chunk)

        if args.demo_small and rows_written >= 300_000:
            break

    clean_df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    if clean_df.empty:
        raise SystemExit("No rows after cleaning (empty dataset?)")

    clean_df.to_parquet(interim_clean, index=False)
    print(f"OK: interim clean written: {interim_clean} rows={len(clean_df)}")

    if args.demo_small:
        top_people = clean_df["person_id"].value_counts().head(50_000).index
        clean_df = clean_df[clean_df["person_id"].isin(top_people)].copy()

    sort_cols = ["person_id"]
    if "start_date" in clean_df.columns:
        sort_cols.append("start_date")

    clean_df = clean_df.sort_values(sort_cols)

    traj = (
        clean_df.groupby("person_id")["job_title_norm"]
        .apply(lambda s: [x for x in s.tolist() if x])
        .reset_index()
        .rename(columns={"job_title_norm": "roles"})
    )

    all_roles = pd.Series([r for seq in traj["roles"] for r in seq], dtype="string").dropna().unique()
    roles_df = pd.DataFrame({"role_name": list(all_roles)})
    roles_df["role_id"] = range(1, len(roles_df) + 1)

    out_traj = paths.processed / "trajectories.parquet"
    out_roles = paths.processed / "roles.parquet"
    traj.to_parquet(out_traj, index=False)
    roles_df.to_parquet(out_roles, index=False)

    print(f"OK: processed trajectories: {out_traj} rows={len(traj)}")
    print(f"OK: processed roles: {out_roles} rows={len(roles_df)}")


if __name__ == "__main__":
    main()
