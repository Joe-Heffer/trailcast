from __future__ import annotations

import os

import httpx


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

    async def fetch_reanalysis(self, lat: float, lon: float) -> dict[str, object]:
        """Fetch historical weather reanalysis data at (lat, lon)."""
        raise NotImplementedError
