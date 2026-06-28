from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SurfaceType = Literal["hardpack", "loam", "clay", "chalk", "gravel"]
Rideability = Literal["good", "fair", "poor", "closed"]


class TrailInput(BaseModel):
    name: str
    gpx_polyline: list[tuple[float, float]]
    surface_type: SurfaceType
    region: str | None = None


class ConditionsForecast(BaseModel):
    trail_name: str
    rideability: Rideability
    confidence: float = Field(ge=0.0, le=1.0)
    forecast_hours: int
    dominant_aspect: str
    notes: list[str]
    generated_at: datetime
