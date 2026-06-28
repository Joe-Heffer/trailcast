from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest

from tests.fixtures.peak_district_polyline import PEAK_DISTRICT_POLYLINE
from trailcast.forecast.engine import ForecastEngine
from trailcast.models import ConditionsForecast, TrailInput
from trailcast.server.app import app
from trailcast.server.dependencies import get_engine

TRAIL_PAYLOAD: dict[str, Any] = {
    "name": "Mam Tor Loop",
    "gpx_polyline": list(PEAK_DISTRICT_POLYLINE),
    "surface_type": "loam",
    "region": "Peak District",
}

TELEMETRY_PAYLOAD: dict[str, Any] = {
    "trail_name": "Mam Tor Loop",
    "gpx_polyline": list(PEAK_DISTRICT_POLYLINE),
    "recorded_at": "2026-06-28T10:00:00+00:00",
    "rider_count": 2,
    "surface_condition": "tacky",
}

MOCK_FORECAST = ConditionsForecast(
    trail=TrailInput(**TRAIL_PAYLOAD),
    rideability="good",
    confidence=0.85,
    forecast_hours=48,
    dominant_aspect="SW",
    notes=["Recent rainfall has improved soil moisture."],
    generated_at=datetime(2026, 6, 28, 10, 0, 0, tzinfo=UTC),
)


@pytest.fixture
def mock_engine() -> ForecastEngine:
    engine = AsyncMock(spec=ForecastEngine)
    engine.run = AsyncMock(return_value=MOCK_FORECAST)
    return engine  # type: ignore[return-value]


@pytest.fixture
def client(mock_engine: ForecastEngine) -> Generator[httpx.AsyncClient, None, None]:
    def override() -> Generator[ForecastEngine, None, None]:
        yield mock_engine

    app.dependency_overrides[get_engine] = override
    yield httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    )
    app.dependency_overrides.clear()


async def test_post_forecast_returns_200(client: httpx.AsyncClient) -> None:
    response = await client.post("/forecast", json=TRAIL_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["rideability"] == "good"
    assert data["trail"]["name"] == "Mam Tor Loop"


async def test_post_forecast_invalid_body_returns_422(client: httpx.AsyncClient) -> None:
    response = await client.post("/forecast", json={"name": "missing fields"})
    assert response.status_code == 422


async def test_post_telemetry_returns_202(client: httpx.AsyncClient) -> None:
    response = await client.post("/telemetry", json=TELEMETRY_PAYLOAD)
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}


async def test_api_key_required_when_env_set(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TRAILCAST_API_KEY", "secret-key")
    response = await client.post("/telemetry", json=TELEMETRY_PAYLOAD)
    assert response.status_code == 403


async def test_api_key_accepted_when_correct(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TRAILCAST_API_KEY", "secret-key")
    response = await client.post(
        "/telemetry",
        json=TELEMETRY_PAYLOAD,
        headers={"X-API-Key": "secret-key"},
    )
    assert response.status_code == 202


async def test_api_key_rejected_when_wrong(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TRAILCAST_API_KEY", "secret-key")
    response = await client.post(
        "/telemetry",
        json=TELEMETRY_PAYLOAD,
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 403
