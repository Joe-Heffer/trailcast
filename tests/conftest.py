import pytest

from tests.fixtures.peak_district_polyline import PEAK_DISTRICT_POLYLINE
from trailcast.models import TrailInput


@pytest.fixture
def trail_input() -> TrailInput:
    return TrailInput(
        name="Mam Tor Loop",
        gpx_polyline=PEAK_DISTRICT_POLYLINE,
        surface_type="loam",
        region="Peak District",
    )
