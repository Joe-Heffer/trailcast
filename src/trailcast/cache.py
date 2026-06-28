from __future__ import annotations

from pathlib import Path

import diskcache

_DEFAULT_CACHE_DIR: Path = Path.home() / ".cache" / "trailcast"


def get_cache(directory: Path | None = None) -> diskcache.Cache:
    cache_dir = directory if directory is not None else _DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    return diskcache.Cache(str(cache_dir))
