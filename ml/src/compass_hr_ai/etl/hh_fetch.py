from __future__ import annotations

import argparse
import time
from typing import Any

import httpx

from compass_hr_ai.utils.cache import cache_json_read, cache_json_write
from compass_hr_ai.utils.paths import DataPaths

HH_BASE = "https://api.hh.ru"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", type=str, required=True, help='Search text, e.g. "data scientist"')
    ap.add_argument("--area", type=int, default=1, help="Area id (1 = Moscow in HH areas)")
    ap.add_argument("--pages", type=int, default=1, help="How many pages to fetch")
    ap.add_argument("--per-page", type=int, default=20, help="Items per page")
    ap.add_argument("--refresh", action="store_true", help="Ignore cache and refetch")
    args = ap.parse_args()

    paths = DataPaths.build()
    out_dir = paths.cache / "hh" / "vacancies"
    out_dir.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Compass-HR-AI-Module (local dev; contact: none)",
        "Accept": "application/json",
    }

    with httpx.Client(base_url=HH_BASE, headers=headers, timeout=60.0) as client:
        for page in range(args.pages):
            params: dict[str, Any] = {
                "text": args.text,
                "area": args.area,
                "page": page,
                "per_page": args.per_page,
            }
            key_payload = {"endpoint": "/vacancies", "params": params}

            if not args.refresh:
                cached = cache_json_read(out_dir, key_payload)
                if cached is not None:
                    print(f"OK: cache hit page={page}")
                    continue

            r = client.get("/vacancies", params=params)
            r.raise_for_status()
            data = r.json()
            cache_json_write(out_dir, key_payload, data)
            print(f"OK: fetched page={page} items={len(data.get('items', []))}")

            time.sleep(0.25)  # gentle rate limit


if __name__ == "__main__":
    main()