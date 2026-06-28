# Trailcast — Claude Code Guide

Predictive trail conditions for mountain biking. Fuses weather, soil type, terrain geometry, and ride-density signals to forecast rideability from a GPS polyline.

## Commands

```bash
# Tests
hatch run test:test

# Lint + format check
hatch run lint:check

# Auto-fix formatting
hatch run lint:fmt

# Type checking
hatch run lint:typecheck
```

## Project layout

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

## Tech stack

- **Build/env**: [Hatch](https://hatch.pypa.io/) — manages virtual envs and scripts; no manual `venv` needed
- **HTTP**: `httpx` with `hishel` for HTTP caching; `stamina` for retries
- **Validation**: Pydantic v2
- **Lint/format**: Ruff (`E`, `W`, `F`, `I`, `UP` rules), line length 100
- **Types**: mypy in strict mode
- **Tests**: pytest + pytest-asyncio (`asyncio_mode = auto`) + hypothesis
- **Python**: 3.11–3.13

## CI

`.github/workflows/ci.yml` runs on every push and PR to `main`:

- **Lint** — `hatch run lint:check` (ruff check + format check)
- **Type Check** — `hatch run lint:typecheck` (mypy strict)
- **Test** — `hatch run test:test` across Python 3.11 and 3.12

All three jobs must pass before merging a PR.

## Releases

`.github/workflows/release.yml` runs `googleapis/release-please-action@v5` on every push to `main`. It reads conventional commit messages to maintain a Release PR, bump the version in `pyproject.toml`, and generate `CHANGELOG.md`.

**All commits to `main` must use [Conventional Commits](https://www.conventionalcommits.org/):**

```
<type>(<scope>): <summary>
```

Common types: `feat`, `fix`, `chore`, `ci`, `docs`, `refactor`, `test`, `perf`.  
A `!` suffix or `BREAKING CHANGE:` footer triggers a major/minor bump.

See [RELEASING.md](RELEASING.md) for the full release process and versioning policy.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `CDS_API_KEY` | Copernicus Climate Data Store key for ERA5 reanalysis |
