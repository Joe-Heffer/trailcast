from __future__ import annotations

import os
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from trailcast.exceptions import APIError, InsufficientDataError, TrailcastError
from trailcast.forecast.engine import ForecastEngine
from trailcast.models import ConditionsForecast, RideTelemetry, TrailInput
from trailcast.server.dependencies import get_engine

app = FastAPI(
    title="trailcast",
    description="Predictive trail conditions for mountain biking.",
    version="0.1.0",
)


# ── Exception handlers ────────────────────────────────────────────────────────


@app.exception_handler(APIError)
async def api_error_handler(_request: Request, exc: APIError) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.BAD_GATEWAY, content={"detail": str(exc)})


@app.exception_handler(InsufficientDataError)
async def insufficient_data_handler(_request: Request, exc: InsufficientDataError) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content={"detail": str(exc)})


@app.exception_handler(TrailcastError)
async def trailcast_error_handler(_request: Request, exc: TrailcastError) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


# ── Auth helper ───────────────────────────────────────────────────────────────


def _verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    required = os.environ.get("TRAILCAST_API_KEY")
    if required and x_api_key != required:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid or missing API key")


# ── Endpoints ─────────────────────────────────────────────────────────────────


@app.post(
    "/forecast",
    response_model=ConditionsForecast,
    dependencies=[Depends(_verify_api_key)],
)
async def forecast(
    trail: TrailInput,
    engine: Annotated[ForecastEngine, Depends(get_engine)],
) -> ConditionsForecast:
    """Generate a rideability forecast for the given trail."""
    return await engine.run(trail)


@app.post(
    "/telemetry",
    status_code=HTTPStatus.ACCEPTED,
    dependencies=[Depends(_verify_api_key)],
)
async def telemetry(ride: RideTelemetry) -> dict[str, str]:
    """Ingest passive ride telemetry from a mobile client."""
    # Stored for future passive-signal model training; acknowledged immediately.
    _ = ride
    return {"status": "accepted"}
