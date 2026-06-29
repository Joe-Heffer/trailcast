# ADR 001: HTTP Service Layer

**Status:** Accepted  
**Date:** 2026-06-28

## Context

trailcast is a Python library and CLI. The mobile app integration requirement (issue #20) cannot be met by a CLI-only interface — mobile clients need an HTTP API to request forecasts and submit passive ride telemetry.

Key constraints:
- The library must remain usable without HTTP dependencies (notebooks, scripts, other services).
- Models (`TrailInput`, `ConditionsForecast`) should be the shared contract between library and API — no translation layer.
- The async design of `ForecastEngine` must be preserved.

## Decision

### Framework: FastAPI

FastAPI is chosen because:
- Native async support matches `ForecastEngine.run()` exactly.
- Pydantic v2 models (`TrailInput`, `ConditionsForecast`, `RideTelemetry`) are reused directly — no serialization boilerplate.
- OpenAPI schema generation is automatic; mobile clients can generate typed SDK clients from it.
- `httpx.ASGITransport` allows in-process integration testing without a running server.

Alternatives considered: Flask (no async-first), Django REST Framework (too heavy), aiohttp (no Pydantic integration, no auto-docs).

### Packaging: `[server]` optional extra

```
pip install trailcast           # pure library — no FastAPI, no uvicorn
pip install trailcast[server]   # adds FastAPI + uvicorn
```

This follows the pattern used by `pydantic[email]`, `sqlalchemy[asyncio]`, and `httpx[http2]`. It ensures that library consumers (data scientists, CI scripts, other services) do not pull in Starlette/uvicorn and their transitive dependencies.

### Authentication: optional API key

If the environment variable `TRAILCAST_API_KEY` is set, every request must supply the matching `X-API-Key` header; otherwise the server runs in unauthenticated development mode. This gives trail associations a simple deployment option (single shared key) without forcing OAuth infrastructure on small operators, while leaving the door open for JWT-based per-association auth in a future iteration.

### Caching: library layer only

Forecast results are cached by the existing `diskcache`-backed transport in `cache.py`. No additional HTTP-layer caching (e.g. Redis) is introduced in this iteration. The expensive DEM + ERA5 computation is guarded at the `ForecastEngine` level, so both CLI and HTTP consumers benefit from the same cache.

### Deployment: Docker + uvicorn

A multi-stage `Dockerfile` produces a minimal `python:3.12-slim` image. Trail associations self-host with:

```
docker run -e TRAILCAST_API_KEY=<key> -p 8000:8000 trailcast-server
```

Minimum infrastructure: a single VM with 1 vCPU and 512 MB RAM is sufficient for low-traffic deployments; CDS_API_KEY must be injected for ERA5 reanalysis.

## Consequences

- `POST /forecast` and `POST /telemetry` are the initial endpoints. `GET /forecast/{trail_id}` requires a persistent trail registry (not yet built) and is deferred.
- The WebSocket `/conditions/stream` endpoint is deferred; it requires a pub/sub backend.
- Adding `fastapi` and `uvicorn` to the `[server]` extra does not affect the base install size.
- mypy strict-mode coverage applies to `src/trailcast/server/` — the server is typed to the same standard as the library.
