from __future__ import annotations

import argparse
import time
from collections.abc import Iterable
from typing import Any

import httpx

from compass_hr_ai.utils.cache import cache_json_read, cache_json_write
from compass_hr_ai.utils.paths import DataPaths

BASE = "https://stepik.org"


def _iter_search_requests(query: str, page: int) -> Iterable[tuple[str, dict[str, Any]]]:
    # Основной вариант: Stepik search API
    yield ("/api/search-results", {"query": query, "page": page})
    yield ("/api/search-results", {"search": query, "page": page})
    yield ("/api/search-results", {"q": query, "page": page})

    # Fallback: иногда пытаются искать по courses (может вернуть пусто, но пусть будет)
    yield ("/api/courses", {"search": query, "page": page})
    yield ("/api/courses", {"query": query, "page": page})
    yield ("/api/courses", {"q": query, "page": page})


def _extract_course_ids(payload: Any) -> list[int]:
    # 1) search-results shape: {"search-results": [{"course": 123}, ...]}
    if isinstance(payload, dict) and isinstance(payload.get("search-results"), list):
        ids: list[int] = []
        for it in payload["search-results"]:
            if isinstance(it, dict):
                v = it.get("course") or it.get("course_id") or it.get("courseId")
                if isinstance(v, int):
                    ids.append(v)
        return sorted(set(ids))

    # 2) courses shape: {"courses": [{"id": 123}, ...]}
    if isinstance(payload, dict) and isinstance(payload.get("courses"), list):
        ids2: list[int] = []
        for c in payload["courses"]:
            if isinstance(c, dict) and isinstance(c.get("id"), int):
                ids2.append(int(c["id"]))
        return sorted(set(ids2))

    return []


def _fetch_json_try_variants(
    client: httpx.Client,
    query: str,
    page: int,
    refresh: bool,
    out_dir,
) -> tuple[list[int], int | None]:
    last_status: int | None = None

    for endpoint, params in _iter_search_requests(query, page):
        key_payload = {"endpoint": endpoint, "params": params}

        if not refresh:
            cached = cache_json_read(out_dir, key_payload)
            if cached is not None:
                ids = _extract_course_ids(cached)
                if ids:
                    return ids, None  # status unknown for cached

        r = client.get(endpoint, params=params)
        last_status = r.status_code
        if r.status_code == 404:
            continue
        r.raise_for_status()
        data = r.json()
        cache_json_write(out_dir, key_payload, data)

        ids = _extract_course_ids(data)
        if ids:
            return ids, r.status_code

    return [], last_status


def _fetch_courses_batch(client: httpx.Client, ids: list[int]) -> dict[str, Any]:
    # Stepik обычно принимает ids[] как повторяющиеся параметры
    params = [("ids[]", str(cid)) for cid in ids]
    r = client.get("/api/courses", params=params, headers={"Accept": "application/json"})
    if r.status_code == 400:
        # fallback: ids=1,2,3
        r = client.get(
            "/api/courses",
            params={"ids": ",".join(str(x) for x in ids)},
            headers={"Accept": "application/json"},
        )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", type=str, default="", help='Search query, e.g. "python"')
    ap.add_argument("--query", type=str, default="", help='Alias for --search, e.g. "python"')
    ap.add_argument("--pages", type=int, default=1, help="How many pages to fetch")
    ap.add_argument("--max-courses", type=int, default=200, help="Hard cap for course details fetch")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    query = (args.search or args.query).strip()
    if not query:
        raise SystemExit("Provide --search or --query")

    paths = DataPaths.build()
    cache_root = paths.cache / "stepik"
    search_dir = cache_root / "search"
    courses_dir = cache_root / "courses"
    search_dir.mkdir(parents=True, exist_ok=True)
    courses_dir.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Compass-HR-AI-Module (local dev; contact: none)",
        "Accept": "application/json",
    }

    all_ids: set[int] = set()

    with httpx.Client(base_url=BASE, headers=headers, timeout=60.0, follow_redirects=True) as client:
        # 1) Search pages -> collect course ids
        for page in range(1, args.pages + 1):
            ids, status = _fetch_json_try_variants(client, query, page, args.refresh, search_dir)
            if ids:
                all_ids.update(ids)
                print(f"OK: search page={page} ids={len(ids)}")
            else:
                print(f"WARN: no ids on page={page} (last_status={status})")
            time.sleep(0.25)

        ids_list = sorted(all_ids)
        if not ids_list:
            raise SystemExit(
                "No course ids found from Stepik API search. "
                "Send first 50 lines of one cached JSON from data/cache/stepik/search/*.json"
            )

        # 2) Fetch course details in batches
        ids_list = ids_list[: args.max_courses]
        batch_size = 50
        fetched_batches = 0

        for i in range(0, len(ids_list), batch_size):
            batch = ids_list[i : i + batch_size]
            key_payload = {"endpoint": "/api/courses", "ids": batch}

            if not args.refresh:
                cached = cache_json_read(courses_dir, key_payload)
                if cached is not None:
                    fetched_batches += 1
                    continue

            data = _fetch_courses_batch(client, batch)
            cache_json_write(courses_dir, key_payload, data)
            fetched_batches += 1
            print(f"OK: fetched courses batch {fetched_batches} (size={len(batch)})")
            time.sleep(0.2)

    print(f"OK: total_course_ids={len(ids_list)}; batches_cached={fetched_batches}")


if __name__ == "__main__":
    main()