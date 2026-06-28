# API Reference

> Placeholder — this document will be generated from docstrings once the
> implementation is in place.

## Schemas

### `TrailInput`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Human-readable trail name |
| `gpx_polyline` | `list[tuple[float, float]]` | Ordered lat/lon pairs |
| `surface_type` | `Literal["hardpack","loam","clay","chalk","gravel"]` | Dominant surface material |
| `region` | `str \| None` | Optional region name for disambiguation |

### `ConditionsForecast`

| Field | Type | Description |
|-------|------|-------------|
| `trail_name` | `str` | Echoes `TrailInput.name` |
| `rideability` | `Literal["good","fair","poor","closed"]` | Overall verdict |
| `confidence` | `float` | Model confidence, 0–1 |
| `forecast_hours` | `int` | Horizon used for the forecast |
| `dominant_aspect` | `str` | Compass direction the trail primarily faces |
| `notes` | `list[str]` | Human-readable explanatory notes |
| `generated_at` | `datetime` | UTC timestamp of forecast generation |

## Exceptions

| Exception | Inherits | When raised |
|-----------|----------|-------------|
| `TrailcastError` | `Exception` | Base — catch-all |
| `APIError` | `TrailcastError` | External API call fails |
| `InsufficientDataError` | `TrailcastError` | Not enough data to forecast |

## Clients

### `OpenMeteoClient`

```python
client = OpenMeteoClient()
data = await client.fetch_forecast(lat=53.37, lon=-1.83, hours=48)
moisture = await client.fetch_soil_moisture(lat=53.37, lon=-1.83)
```

### `SoilGridsClient`

```python
client = SoilGridsClient()
soil = await client.fetch_soil_properties(lat=53.37, lon=-1.83)
```

### `ERA5Client`

```python
# Reads CDS_API_KEY from environment
client = ERA5Client()
reanalysis = await client.fetch_reanalysis(lat=53.37, lon=-1.83)
```

### `TerrainAnalyzer`

```python
analyzer = TerrainAnalyzer()
twi = analyzer.compute_twi(lat=53.37, lon=-1.83)
aspect = analyzer.compute_aspect(lat=53.37, lon=-1.83)  # e.g. "NW"
slope = analyzer.compute_slope(lat=53.37, lon=-1.83)    # degrees
```

### `ForecastEngine`

```python
engine = ForecastEngine()
forecast = await engine.run(trail, hours=48)
```
