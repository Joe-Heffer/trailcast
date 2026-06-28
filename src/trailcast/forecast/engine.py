from __future__ import annotations

from trailcast.models import ConditionsForecast, TrailInput


class ForecastEngine:
    """Orchestrates terrain, weather, and soil signals into a rideability forecast."""

    async def run(self, trail: TrailInput, hours: int = 48) -> ConditionsForecast:
        """Produce a rideability forecast for *trail* over the next *hours* hours."""
        raise NotImplementedError
