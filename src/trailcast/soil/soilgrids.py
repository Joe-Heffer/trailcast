from __future__ import annotations

import httpx
from pydantic import BaseModel, ConfigDict


class SoilProperties(BaseModel):
    """Parsed response from the ISRIC SoilGrids API."""

    model_config = ConfigDict(extra="ignore")

    sand_fraction: float  # 0–1 mass fraction
    silt_fraction: float
    clay_fraction: float
    usda_class: str  # e.g. "Sandy loam"


class SoilGridsClient:
    """Async client for the ISRIC SoilGrids REST API.

    Returns soil texture and type data at a GPS point. Free, no key required.
    Docs: https://rest.isric.org/soilgrids/v2.0/docs
    """

    BASE_URL = "https://rest.isric.org/soilgrids/v2.0"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def fetch_soil_properties(self, lat: float, lon: float) -> SoilProperties:
        """Fetch soil texture and classification at (lat, lon)."""
        raise NotImplementedError
