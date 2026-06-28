from __future__ import annotations

from pathlib import Path

import hishel

_DEFAULT_CACHE_DIR: Path = Path.home() / ".cache" / "trailcast"


def make_cache_transport(
    directory: Path | None = None,
) -> hishel.AsyncCacheTransport:
    """Return an httpx-compatible async cache transport backed by disk storage.

    Inject into ``httpx.AsyncClient(transport=make_cache_transport())`` so that
    HTTP responses are cached on disk and reused across runs, respecting standard
    Cache-Control / ETag semantics automatically.
    """
    cache_dir = directory if directory is not None else _DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    storage = hishel.FileStorage(base_path=cache_dir)
    return hishel.AsyncCacheTransport(
        transport=hishel.AsyncHTTPTransport(),
        storage=storage,
    )
