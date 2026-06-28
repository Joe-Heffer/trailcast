[![CI](https://github.com/Joe-Heffer/trailcast/actions/workflows/ci.yml/badge.svg)](https://github.com/Joe-Heffer/trailcast/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Joe-Heffer/trailcast/branch/main/graph/badge.svg)](https://codecov.io/gh/Joe-Heffer/trailcast)

# trailcast

**Predictive trail conditions for mountain biking.** `trailcast` fuses weather forecasts, soil type, terrain geometry (slope, aspect, TWI), and ride-density signals to produce a rideability forecast from a GPS polyline. Open-source infrastructure for local clubs, trail associations, and MTB apps.

---

## Install

```bash
pip install trailcast
```

For terrain analysis (requires C++ build tools and optionally GDAL):

```bash
pip install "trailcast[terrain-full]"
```

> **Note — `richdem`** has a C++ build dependency and may fail on some systems.
> If installation fails, `xarray-spatial` provides equivalent TWI/slope/aspect
> functionality and can be used as a drop-in fallback.
>
> **Note — `pysheds`** requires `rasterio`, which in turn requires GDAL.
> On Ubuntu/Debian: `sudo apt-get install libgdal-dev` before installing.

## Usage

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
        # … more lat/lon pairs
    ],
    surface_type="loam",
    region="Peak District",
)

# Prediction logic is not yet implemented — coming soon.
engine = ForecastEngine()
# forecast = asyncio.run(engine.run(trail, hours=48))
# print(forecast.rideability)   # "good" | "fair" | "poor" | "closed"
# print(forecast.confidence)    # 0.0 – 1.0
```

## External APIs

| API | Purpose | Key required |
|-----|---------|--------------|
| [Open-Meteo](https://open-meteo.com/) | Weather + soil moisture forecast | No |
| [SoilGrids](https://www.isric.org/explore/soilgrids) | Soil texture at a GPS point | No |
| [ERA5 / CDS API](https://cds.climate.copernicus.eu/) | Historical weather reanalysis | Yes — set `CDS_API_KEY` |

Copy `.env.example` to `.env` and fill in your keys before running anything that touches ERA5.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to set up the dev environment, run tests, and submit a PR.

## License

MIT — see [LICENSE](LICENSE).
