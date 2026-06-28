from __future__ import annotations

import httpx


class OpenMeteoClient:
    """Async client for the Open-Meteo weather and soil-moisture forecast API.

    Open-Meteo is free and requires no API key.
    Docs: https://open-meteo.com/en/docs
    """

    BASE_URL = "https://api.open-meteo.com/v1"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def fetch_forecast(self, lat: float, lon: float, hours: int = 48) -> dict[str, object]:
        """Fetch hourly weather forecast for the given coordinates."""
        raise NotImplementedError

    async def fetch_soil_moisture(self, lat: float, lon: float) -> dict[str, object]:
        """Fetch soil moisture forecast for the given coordinates."""
        raise NotImplementedError
