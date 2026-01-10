from __future__ import annotations

import subprocess

from compass_hr_ai.utils.paths import DataPaths


def run(cmd: list[str]) -> None:
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    paths = DataPaths.build()

    # Rostrud demo run
    run(["python", "-m", "compass_hr_ai.etl.rostrud_ingest", "--demo-small"])

    # HH tiny fetch+parse (1 page)
    run(["python", "-m", "compass_hr_ai.etl.hh_fetch", "--text", "data scientist", "--area", "1", "--pages", "1", "--per-page", "20"])
    run(["python", "-m", "compass_hr_ai.etl.hh_parse"])

    # Stepik tiny fetch+parse (1 page)
    run(["python", "-m", "compass_hr_ai.etl.stepik_fetch", "--search", "python", "--pages", "1"])
    run(["python", "-m", "compass_hr_ai.etl.stepik_parse"])

    expected = [
        paths.processed / "trajectories.parquet",
        paths.processed / "roles.parquet",
        paths.processed / "hh_vacancies.parquet",
        paths.processed / "courses.parquet",
    ]
    missing = [p for p in expected if not p.exists()]
    if missing:
        raise SystemExit(f"Missing outputs: {missing}")

    print("OK: ETL smoke passed")
    for p in expected:
        print("OK:", p)


if __name__ == "__main__":
    main()
