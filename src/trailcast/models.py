from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# (latitude, longitude) in decimal degrees — WGS-84
LatLon = tuple[float, float]

SurfaceType = Literal["hardpack", "loam", "clay", "chalk", "gravel"]
Rideability = Literal["good", "fair", "poor", "closed"]
Aspect = Literal["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class TrailInput(BaseModel):
    name: str
    gpx_polyline: list[LatLon]
    surface_type: SurfaceType
    region: str | None = None


class TerrainResult(BaseModel):
    dominant_aspect: Aspect
    mean_slope: float  # degrees
    mean_twi: float


class ConditionsForecast(BaseModel):
    trail: TrailInput
    rideability: Rideability
    confidence: float = Field(ge=0.0, le=1.0)
    forecast_hours: int
    dominant_aspect: Aspect
    notes: list[str]
    generated_at: datetime

    @field_validator("generated_at")
    @classmethod
    def must_be_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("generated_at must be timezone-aware (use datetime.now(tz=UTC))")
        return v
