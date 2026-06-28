# Architecture

> Placeholder — this document will describe the end-to-end data flow from GPS polyline to rideability forecast.

## Overview

```
TrailInput (GPS polyline + surface type)
        │
        ├─► terrain/   TWI, slope, dominant aspect
        ├─► weather/   hourly precipitation, temperature, wind (Open-Meteo)
        ├─► soil/      texture, drainage class (SoilGrids + ERA5)
        │
        └─► forecast/  ForecastEngine → ConditionsForecast
```

## Submodules

### `terrain/`

Computes topographic wetness index (TWI), slope, and aspect from a DEM
covering the trail's bounding box. Uses `richdem` (or `xarray-spatial` as
fallback) for raster terrain analysis.

### `weather/`

Fetches current and forecast weather via Open-Meteo. No API key required.
Covers precipitation accumulation, temperature, wind speed, and volumetric
soil water content.

### `soil/`

- **SoilGrids** — REST API for soil texture (sand/silt/clay fractions) and
  USDA soil class at a GPS point.
- **ERA5** — Historical precipitation reanalysis via the Copernicus CDS API.
  Used to compute antecedent soil moisture. Requires `CDS_API_KEY`.

### `forecast/`

`ForecastEngine` orchestrates signals from the three sources above and applies
the conditions model (see `conditions-model.md`) to produce a `ConditionsForecast`.

### `cli/`

A `typer`-based CLI aimed at trail stewards. Accepts a trail name and optional
region, looks up the trail's polyline from a local config, and prints the
forecast to stdout.

### `cache/`

`diskcache`-backed caching layer for slow or rate-limited API responses
(primarily SoilGrids, which changes rarely). Default cache dir:
`~/.cache/trailcast/`.
