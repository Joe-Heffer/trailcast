from trailcast.weather import OpenMeteoClient


def test_open_meteo_client_importable() -> None:
    assert OpenMeteoClient is not None


def test_open_meteo_client_instantiable() -> None:
    client = OpenMeteoClient()
    assert isinstance(client, OpenMeteoClient)
