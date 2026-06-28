from __future__ import annotations

try:
    import richdem  # noqa: F401

    _RICHDEM_AVAILABLE: bool = True
except ImportError:
    _RICHDEM_AVAILABLE = False
    # richdem not installed — install trailcast[terrain-full] or use xarray-spatial


class TerrainAnalyzer:
    """Computes terrain attributes (TWI, aspect, slope) from a GPS bounding box."""

    def compute_twi(self, lat: float, lon: float) -> float:
        """Return the topographic wetness index at (lat, lon)."""
        raise NotImplementedError

    def compute_aspect(self, lat: float, lon: float) -> str:
        """Return the dominant aspect as a compass direction (e.g. 'NW')."""
        raise NotImplementedError

    def compute_slope(self, lat: float, lon: float) -> float:
        """Return the slope in degrees at (lat, lon)."""
        raise NotImplementedError
