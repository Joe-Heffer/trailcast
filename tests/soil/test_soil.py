from trailcast.soil import ERA5Client, SoilGridsClient


def test_soil_clients_importable() -> None:
    assert SoilGridsClient is not None
    assert ERA5Client is not None


def test_soilgrids_client_instantiable() -> None:
    client = SoilGridsClient()
    assert isinstance(client, SoilGridsClient)


def test_era5_client_instantiable() -> None:
    client = ERA5Client()
    assert isinstance(client, ERA5Client)
