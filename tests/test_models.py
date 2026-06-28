from datetime import UTC, datetime

from trailcast.models import ConditionsForecast, TrailInput


def test_trail_input_validates(trail_input: TrailInput) -> None:
    assert trail_input.name == "Mam Tor Loop"
    assert trail_input.surface_type == "loam"
    assert trail_input.region == "Peak District"
    assert len(trail_input.gpx_polyline) == 12


def test_conditions_forecast_validates() -> None:
    forecast = ConditionsForecast(
        trail_name="Mam Tor Loop",
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
