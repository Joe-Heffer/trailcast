from __future__ import annotations

import os

import httpx
from pydantic import BaseModel, ConfigDict


class ERA5Reanalysis(BaseModel):
    """Parsed response from the Copernicus CDS ERA5 reanalysis endpoint."""

    model_config = ConfigDict(extra="ignore")

    accumulated_precipitation_mm: float  # mm over the analysis period
    mean_temperature_c: float  # °C


class ERA5Client:
    """Async client for ERA5 historical weather reanalysis via the CDS API.

    Requires a Copernicus Climate Data Store API key set via the
    ``CDS_API_KEY`` environment variable (or passed directly).
    Register at: https://cds.climate.copernicus.eu/
    """

    def __init__(
        self,
        api_key: str | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key or os.environ.get("CDS_API_KEY")
        self._client = client

    async def fetch_reanalysis(self, lat: float, lon: float) -> ERA5Reanalysis:
        """Fetch historical weather reanalysis data at (lat, lon)."""
        raise NotImplementedError
