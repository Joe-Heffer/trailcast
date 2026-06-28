from __future__ import annotations

from trailcast.models import ConditionsForecast, TrailInput
from trailcast.soil.era5 import ERA5Client
from trailcast.soil.soilgrids import SoilGridsClient
from trailcast.terrain.analyzer import TerrainAnalyzer
from trailcast.weather.client import OpenMeteoClient


class ForecastEngine:
    """Orchestrates terrain, weather, and soil signals into a rideability forecast."""

    def __init__(
        self,
        weather_client: OpenMeteoClient | None = None,
        soil_client: SoilGridsClient | None = None,
        era5_client: ERA5Client | None = None,
        terrain_analyzer: TerrainAnalyzer | None = None,
    ) -> None:
        self._weather = weather_client or OpenMeteoClient()
        self._soil = soil_client or SoilGridsClient()
        self._era5 = era5_client or ERA5Client()
        self._terrain = terrain_analyzer or TerrainAnalyzer()

    async def run(self, trail: TrailInput, hours: int = 48) -> ConditionsForecast:
        """Produce a rideability forecast for *trail* over the next *hours* hours."""
        raise NotImplementedError
