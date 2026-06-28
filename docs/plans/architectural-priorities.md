# Architectural priorities

This document captures the architectural decisions that should be made or resolved before the core implementation grows further. Derived from the open GitHub issues as of 2026-06-28.

## Must decide before building more

### 1. HTTP service layer (issue #20)

The library-only architecture cannot serve a mobile app. FastAPI is the natural choice given the async-first design and Pydantic model reuse already in place.

This decision shapes caching strategy, authentication, rate limiting, and how the telemetry ingestion endpoint is structured. It should be resolved before implementing the core pipeline (issue #12), not after, because the service boundary changes what the engine's async surface needs to look like.

Minimum viable endpoints:
- `POST /forecast` — accepts `TrailInput`, returns `ConditionsForecast`
- `GET /forecast/{trail_id}` — cached forecast for a registered trail
- `POST /telemetry` — ingest ride telemetry for passive conditions signal

### 2. Telemetry ingestion pipeline and privacy boundary (issue #22)

The anonymisation approach for GPS tracks must be specified before any ride data is stored. Retrofitting anonymisation onto stored data is a legal and trust problem.

This design decision is foundational to:
- Issue #15 (passive conditions signal from ride telemetry)
- Issue #16 (absence-of-activity signal)
- Issue #28 (post-ride conditions contribution)

The architecture decision record must cover: anonymisation method, aggregation window, retention period, and the ingest path (HTTP endpoint vs. message queue).

### 3. Offline-first bundle format (issue #21)

Committing to a bundle format (forecast JSON + terrain summary + GPX + map tiles) early prevents the mobile client from becoming coupled to a live API. If this is not specified before the HTTP service layer is built, offline capability gets bolted on rather than designed in.

Candidate format: a ZIP bundle with an expiry timestamp; MBTiles for map tiles (SQLite-backed, widely supported). A `trailcast bundle export` CLI command provides the reference implementation.

## Foundational model changes (cheap now, expensive later)

### 4. Confidence source attribution in `ConditionsForecast` (issue #17)

Adding `confidence_sources` (list of `ConfidenceSource` models) and `confidence_summary` (human-readable string) to `ConditionsForecast` should happen alongside implementing `ForecastEngine.run()` (issue #12), not after. Every downstream consumer — CLI, HTTP API, mobile client — will need to display or forward this field. Changing the model after the API is live requires versioning.

### 5. Adaptive trail fields in `TrailInput` (issue #18)

Adding optional fields for adaptive riders (path width, surface hardness, gradient profile, wheelchair accessible, `last_verified_at`) costs almost nothing at this stage. Adding them after the HTTP API is live and clients are serialising the model requires a versioned schema change.

All fields are optional, so existing integrations are unaffected.

## Suggested sequencing

```
#20 (HTTP service layer)
  → #22 (telemetry privacy architecture)
  → #17 (confidence attribution, alongside #12)
  → #18 (adaptive fields, alongside #12)
  → #21 (offline bundle format)
  → core pipeline: #7, #8, #10, #11, #12, #14
```

## Deferred (correct direction, not blocking current work)

**Issue #35 — Privacy-positive social architecture** and **issue #36 — Competitive feature isolation (Pattern 8)** are the right structural commitments, but they apply to a social and mobile phase that depends on the ride-recording layer. They should be revisited before any social or competitive feature work begins.

**Issue #23 (rider ability profile)** and **issue #24 (ride character model)** belong to the ride-recording layer, which depends on the `RideRecord` model (issue #26) first.
