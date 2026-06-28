from __future__ import annotations

from trailcast.models import LatLon, TerrainResult

try:
    import richdem  # noqa: F401

    _RICHDEM_AVAILABLE: bool = True
except ImportError:
    _RICHDEM_AVAILABLE = False
    # richdem not installed — install trailcast[terrain-full] or use xarray-spatial


class TerrainAnalyzer:
    """Computes terrain attributes (TWI, slope, aspect) from a GPS polyline."""

    def compute_terrain(self, polyline: list[LatLon]) -> TerrainResult:
        """Return aggregated terrain attributes for the full trail polyline.

        Fetches the DEM once for the polyline's bounding box, then derives
        dominant aspect, mean slope (degrees), and mean TWI across all points.
        """
        raise NotImplementedError
