from __future__ import annotations

from collections.abc import Generator

from trailcast.forecast.engine import ForecastEngine

_engine: ForecastEngine | None = None


def get_engine() -> Generator[ForecastEngine, None, None]:
    """Yield a module-level shared ForecastEngine (instantiated once per process)."""
    global _engine
    if _engine is None:
        _engine = ForecastEngine()
    yield _engine
