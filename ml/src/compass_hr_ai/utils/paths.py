from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def repo_root() -> Path:
    # .../Compass-HR-AI-Module/ml/src/compass_hr_ai/utils/paths.py
    # parents: utils -> compass_hr_ai -> src -> ml -> REPO
    return Path(__file__).resolve().parents[4]


def data_dir() -> Path:
    return repo_root() / "data"


def raw_dir() -> Path:
    return data_dir() / "raw"


def interim_dir() -> Path:
    return data_dir() / "interim"


def processed_dir() -> Path:
    return data_dir() / "processed"


def cache_dir() -> Path:
    return data_dir() / "cache"


@dataclass(frozen=True)
class DataPaths:
    repo: Path
    data: Path
    raw: Path
    interim: Path
    processed: Path
    cache: Path

    @staticmethod
    def build() -> DataPaths:
        r = repo_root()
        d = data_dir()
        return DataPaths(
            repo=r,
            data=d,
            raw=raw_dir(),
            interim=interim_dir(),
            processed=processed_dir(),
            cache=cache_dir(),
        )
