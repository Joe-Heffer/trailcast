from trailcast.terrain import TerrainAnalyzer


def test_terrain_analyzer_importable() -> None:
    assert TerrainAnalyzer is not None


def test_terrain_analyzer_instantiable() -> None:
    analyzer = TerrainAnalyzer()
    assert isinstance(analyzer, TerrainAnalyzer)
