from pathlib import Path

import hishel

from trailcast.cache import make_cache_transport


def test_make_cache_transport_returns_transport(tmp_path: Path) -> None:
    transport = make_cache_transport(tmp_path)
    assert isinstance(transport, hishel.AsyncCacheTransport)


def test_make_cache_transport_creates_directory(tmp_path: Path) -> None:
    cache_dir = tmp_path / "nested" / "cache"
    make_cache_transport(cache_dir)
    assert cache_dir.exists()
