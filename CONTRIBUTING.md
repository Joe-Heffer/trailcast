# Contributing to trailcast

## Dev environment setup

Prerequisites: Python 3.11+, [Hatch](https://hatch.pypa.io/latest/install/).

```bash
pip install hatch
git clone https://github.com/joe-heffer/trailcast.git
cd trailcast
```

Hatch manages virtual environments automatically — no manual `venv` needed.

### Optional terrain dependencies

To work on terrain analysis features you'll need the `terrain-full` extra.
On some systems this requires system-level libraries:

```bash
# Ubuntu/Debian — for pysheds (rasterio → GDAL)
sudo apt-get install libgdal-dev

pip install "trailcast[terrain-full]"
```

If `richdem` fails to build, install `xarray-spatial` as a fallback:

```bash
pip install xarray-spatial
```

## Running tests

```bash
hatch run test:test
```

Run with coverage:

```bash
hatch run test:test --cov=src/trailcast --cov-report=term-missing
```

Run a specific file or test:

```bash
hatch run test:test tests/test_models.py
hatch run test:test -k test_trail_input_validates
```

## Linting and formatting

Check for lint errors and formatting issues:

```bash
hatch run lint:check
```

Auto-fix formatting:

```bash
hatch run lint:fmt
```

## Type checking

```bash
hatch run lint:typecheck
```

## Environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Purpose |
|----------|---------|
| `CDS_API_KEY` | Copernicus Climate Data Store key for ERA5 reanalysis |

## Project structure

```
src/trailcast/
├── models.py       Pydantic input/output schemas
├── exceptions.py   Custom exception hierarchy
├── cache.py        diskcache wrapper for slow API responses
├── terrain/        TWI, slope, aspect from GPS bounding box
├── weather/        Open-Meteo client (weather + soil moisture)
├── soil/           SoilGrids and ERA5 clients
├── forecast/       Forecast engine (orchestrates the above)
└── cli/            typer CLI for trail stewards
```

## Submitting a PR

1. Fork the repo and create a branch: `git checkout -b feat/your-feature`
2. Make your changes and add tests
3. Ensure `hatch run lint:check` and `hatch run test:test` both pass
4. Open a PR against `main`
