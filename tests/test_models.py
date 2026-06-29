from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from trailcast.models import ConditionsForecast, RideTelemetry, TrailInput


def test_trail_input_validates(trail_input: TrailInput) -> None:
    assert trail_input.name == "Mam Tor Loop"
    assert trail_input.surface_type == "loam"
    assert trail_input.region == "Peak District"
    assert len(trail_input.gpx_polyline) == 12


def test_conditions_forecast_validates(trail_input: TrailInput) -> None:
    forecast = ConditionsForecast(
        trail=trail_input,
        rideability="good",
        confidence=0.85,
        forecast_hours=48,
        dominant_aspect="NW",
        notes=["Dry for 72 h", "Sandy loam drains well"],
        generated_at=datetime.now(tz=UTC),
    )
    assert forecast.rideability == "good"
    assert 0.0 <= forecast.confidence <= 1.0
    assert forecast.forecast_hours == 48
    assert forecast.trail.name == "Mam Tor Loop"


def test_conditions_forecast_rejects_naive_datetime(trail_input: TrailInput) -> None:
    with pytest.raises(ValidationError, match="timezone-aware"):
        ConditionsForecast(
            trail=trail_input,
            rideability="good",
            confidence=0.85,
            forecast_hours=48,
            dominant_aspect="NW",
            notes=[],
            generated_at=datetime.now(),  # naive — no tz
        )


def test_ride_telemetry_validates() -> None:
    telemetry = RideTelemetry(
        trail_name="Mam Tor Loop",
        gpx_polyline=[(53.368, -1.802)],
        recorded_at=datetime.now(tz=UTC),
    )
    assert telemetry.trail_name == "Mam Tor Loop"
    assert telemetry.recorded_at.tzinfo is not None


def test_ride_telemetry_rejects_naive_datetime() -> None:
    with pytest.raises(ValidationError, match="timezone-aware"):
        RideTelemetry(
            trail_name="Mam Tor Loop",
            gpx_polyline=[(53.368, -1.802)],
            recorded_at=datetime.now(),  # naive — no tz
        )
