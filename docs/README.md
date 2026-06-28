# trailcast Documentation

**trailcast** predicts mountain biking trail conditions by fusing weather forecasts, soil data,
terrain geometry, and ride-density signals into a single rideability verdict for any GPS polyline.

## Table of contents

- [Architecture](architecture.md) — end-to-end data flow from GPS input to forecast output
- [Conditions model](conditions-model.md) — how terrain, weather, and soil signals combine into a rideability verdict
- [API reference](api-reference.md) — Python API for `TrailInput`, `ForecastEngine`, and `ConditionsForecast`

---

## Quick start

### Install

```bash
pip install trailcast
```

For terrain analysis (requires C++ build tools and optionally GDAL):

```bash
pip install "trailcast[terrain-full]"
```

### Python API

```python
import asyncio
from trailcast.models import TrailInput
from trailcast.forecast import ForecastEngine

trail = TrailInput(
    name="Mam Tor Loop",
    gpx_polyline=[
        (53.3706, -1.8346),
        (53.3720, -1.8295),
        (53.3742, -1.8225),
    ],
    surface_type="loam",
    region="Peak District",
)

engine = ForecastEngine()
forecast = asyncio.run(engine.run(trail, hours=48))

print(forecast.rideability)   # "good" | "fair" | "poor" | "closed"
print(forecast.confidence)    # 0.0 – 1.0
print(forecast.notes)         # list of human-readable condition notes
```

### CLI

```bash
# Forecast by trail name (looks up polyline from ~/.trailcast/trails.json)
trailcast forecast "Mam Tor Loop" --region "Peak District"

# Supply a GPX file directly
trailcast forecast "Mam Tor Loop" --gpx trail.gpx --hours 72
```

---

## Rideability levels

| Level | Meaning |
|-------|---------|
| `good` | Optimal — minimal mud risk, firm surface |
| `fair` | Rideable but imperfect — some mud likely, take care |
| `poor` | High mud risk or slow-drying surface — consider alternatives |
| `closed` | Closure recommended — significant trail damage risk |

---

## External APIs

| API | Purpose | Key required |
|-----|---------|--------------|
| [Open-Meteo](https://open-meteo.com/) | Hourly weather + soil moisture forecast | No |
| [SoilGrids](https://www.isric.org/explore/soilgrids) | Soil texture (sand/silt/clay) at a GPS point | No |
| [ERA5 / CDS API](https://cds.climate.copernicus.eu/) | Historical precipitation reanalysis | Yes — `CDS_API_KEY` |

Copy `.env.example` to `.env` and set `CDS_API_KEY` before running anything that touches ERA5.

---

## Data model

### Input — `TrailInput`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Trail name |
| `gpx_polyline` | `list[tuple[float, float]]` | Ordered `(lat, lon)` pairs in WGS-84 |
| `surface_type` | `"hardpack" \| "loam" \| "clay" \| "chalk" \| "gravel"` | Dominant surface material |
| `region` | `str \| None` | Optional region name for display |

### Output — `ConditionsForecast`

| Field | Type | Description |
|-------|------|-------------|
| `rideability` | `Rideability` | Four-level verdict (see above) |
| `confidence` | `float` | 0.0 – 1.0 confidence score |
| `forecast_hours` | `int` | Horizon used for the forecast |
| `dominant_aspect` | `Aspect` | Cardinal/ordinal compass direction of the trail |
| `notes` | `list[str]` | Human-readable condition notes |
| `generated_at` | `datetime` | Timezone-aware timestamp of forecast generation |

---

## Development

Prerequisites: Python 3.11+, [Hatch](https://hatch.pypa.io/).

```bash
git clone https://github.com/joe-heffer/trailcast.git
cd trailcast
```

Hatch manages virtual environments automatically — no manual `venv` needed.

```bash
# Run tests
hatch run test:test

# Lint + format check
hatch run lint:check

# Auto-fix formatting
hatch run lint:fmt

# Type checking
hatch run lint:typecheck
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contributor guide.
