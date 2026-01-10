from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def _stable_key(payload: Mapping[str, Any]) -> str:
    dumped = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(dumped.encode("utf-8")).hexdigest()


def cache_json_write(dir_path: Path, key_payload: Mapping[str, Any], data: Any) -> Path:
    dir_path.mkdir(parents=True, exist_ok=True)
    key = _stable_key(key_payload)
    out = dir_path / f"{key}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def cache_json_read(dir_path: Path, key_payload: Mapping[str, Any]) -> Any | None:
    key = _stable_key(key_payload)
    p = dir_path / f"{key}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))
