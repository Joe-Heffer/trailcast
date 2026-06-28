# Conditions Model

> Placeholder — this document will describe how trailcast combines terrain,
> weather, and soil signals into a rideability verdict.

## Rideability levels

| Level | Meaning |
|-------|---------|
| `good` | Optimal conditions — minimal mud risk, firm surface |
| `fair` | Rideable but imperfect — some mud likely, take care |
| `poor` | High mud risk or slow-drying surface — consider alternatives |
| `closed` | Closure recommended — significant trail damage risk |

## Planned signal weights

The following factors will be combined into the final verdict. Exact
coefficients are TBD pending calibration against field observations.

### Weather signals
- Accumulated precipitation (past 48 h, forecast 48 h)
- Antecedent soil moisture (ERA5 reanalysis)
- Air temperature (freeze/thaw cycles)

### Terrain signals
- Topographic Wetness Index (TWI) — higher TWI → slower drying
- Slope — steeper slopes shed water faster
- Dominant aspect — north-facing aspects dry slower at mid-latitudes

### Soil signals
- Sand/silt/clay fractions from SoilGrids
- USDA soil drainage class
- User-supplied `surface_type` override

## Calibration

The model will initially use literature-derived heuristics. Once enough
labelled condition reports are collected from trail stewards, the weights
will be tuned via a regression or gradient-boosted model trained on
historical forecasts + observed conditions.
