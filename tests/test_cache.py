from pathlib import Path

import diskcache

from trailcast.cache import get_cache


def test_get_cache_returns_cache_instance(tmp_path: Path) -> None:
    cache = get_cache(tmp_path)
    assert isinstance(cache, diskcache.Cache)
    cache.close()


def test_get_cache_creates_directory(tmp_path: Path) -> None:
    cache_dir = tmp_path / "nested" / "cache"
    cache = get_cache(cache_dir)
    assert cache_dir.exists()
    cache.close()
