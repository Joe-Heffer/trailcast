from trailcast.forecast import ForecastEngine


def test_forecast_engine_importable() -> None:
    assert ForecastEngine is not None


def test_forecast_engine_instantiable() -> None:
    engine = ForecastEngine()
    assert isinstance(engine, ForecastEngine)
