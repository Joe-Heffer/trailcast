# API Reference

> Placeholder — this document will be generated from docstrings once the
> implementation is in place.

## Type aliases

| Alias | Definition | Notes |
|-------|-----------|-------|
| `LatLon` | `tuple[float, float]` | `(latitude, longitude)` in decimal degrees, WGS-84 |
| `SurfaceType` | `Literal["hardpack","loam","clay","chalk","gravel"]` | Dominant surface material |
| `Rideability` | `Literal["good","fair","poor","closed"]` | Overall rideability verdict |
| `Aspect` | `Literal["N","NE","E","SE","S","SW","W","NW"]` | Compass direction |

All type aliases are importable directly from `trailcast`:

```python
from trailcast import SurfaceType, Rideability
```

## Schemas

### `TrailInput`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Human-readable trail name |
| `gpx_polyline` | `list[LatLon]` | Ordered `(lat, lon)` pairs — WGS-84 |
| `surface_type` | `SurfaceType` | Dominant surface material |
| `region` | `str \| None` | Optional region name for disambiguation |

### `ConditionsForecast`

| Field | Type | Description |
|-------|------|-------------|
| `trail` | `TrailInput` | The input trail this forecast was generated for |
| `rideability` | `Rideability` | Overall verdict |
| `confidence` | `float` | Model confidence, 0–1 |
| `forecast_hours` | `int` | Horizon used for the forecast |
| `dominant_aspect` | `Aspect` | Compass direction the trail primarily faces |
| `notes` | `list[str]` | Human-readable explanatory notes |
| `generated_at` | `datetime` | UTC timestamp of forecast generation (must be timezone-aware) |

### `TerrainResult`

Returned by `TerrainAnalyzer.compute_terrain()`.

| Field | Type | Description |
|-------|------|-------------|
| `dominant_aspect` | `Aspect` | Dominant compass aspect across the polyline |
| `mean_slope` | `float` | Mean slope in degrees |
| `mean_twi` | `float` | Mean topographic wetness index |

## Exceptions

| Exception | Inherits | When raised |
|-----------|----------|-------------|
| `TrailcastError` | `Exception` | Base — catch-all |
| `APIError` | `TrailcastError` | External API call fails |
| `InsufficientDataError` | `TrailcastError` | Not enough data to forecast |

## Clients

### `OpenMeteoClient`

Returns typed `WeatherForecast` models (defined in `trailcast.weather`).

```python
client = OpenMeteoClient()
forecast = await client.fetch_forecast(lat=53.37, lon=-1.83, hours=48)
moisture = await client.fetch_soil_moisture(lat=53.37, lon=-1.83)
```

### `SoilGridsClient`

Returns a `SoilProperties` model (defined in `trailcast.soil`).

```python
client = SoilGridsClient()
soil = await client.fetch_soil_properties(lat=53.37, lon=-1.83)
```

### `ERA5Client`

Returns an `ERA5Reanalysis` model (defined in `trailcast.soil`).

```python
# Reads CDS_API_KEY from environment
client = ERA5Client()
reanalysis = await client.fetch_reanalysis(lat=53.37, lon=-1.83)
```

### `TerrainAnalyzer`

Accepts the full polyline and fetches the DEM once for the bounding box.

```python
analyzer = TerrainAnalyzer()
terrain = analyzer.compute_terrain(polyline=trail.gpx_polyline)
# terrain.dominant_aspect → "NW"
# terrain.mean_slope      → 12.4  (degrees)
# terrain.mean_twi        → 6.8
```

### `ForecastEngine`

All sub-clients are optional; the engine creates defaults if omitted. Inject
custom instances to control caching, timeouts, or to swap in test doubles.

```python
engine = ForecastEngine(
    weather_client=OpenMeteoClient(client=cached_http_client),
    era5_client=ERA5Client(api_key="..."),
)
forecast = await engine.run(trail, hours=48)
```
