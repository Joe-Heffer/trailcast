from __future__ import annotations

import httpx
from pydantic import BaseModel, ConfigDict, Field


class HourlyWeather(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: list[str]
    precipitation: list[float] = Field(default_factory=list)  # mm
    temperature_2m: list[float] = Field(default_factory=list)  # °C
    wind_speed_10m: list[float] = Field(default_factory=list)  # km/h
    soil_moisture_0_to_1cm: list[float] = Field(default_factory=list)  # m³/m³


class WeatherForecast(BaseModel):
    """Parsed response from the Open-Meteo forecast or soil-moisture endpoint."""

    model_config = ConfigDict(extra="ignore")

    latitude: float
    longitude: float
    hourly: HourlyWeather


class OpenMeteoClient:
    """Async client for the Open-Meteo weather and soil-moisture forecast API.

    Open-Meteo is free and requires no API key.
    Docs: https://open-meteo.com/en/docs
    """

    BASE_URL = "https://api.open-meteo.com/v1"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def fetch_forecast(self, lat: float, lon: float, hours: int = 48) -> WeatherForecast:
        """Fetch hourly weather forecast for the given coordinates."""
        raise NotImplementedError

    async def fetch_soil_moisture(self, lat: float, lon: float) -> WeatherForecast:
        """Fetch soil moisture forecast for the given coordinates."""
        raise NotImplementedError
