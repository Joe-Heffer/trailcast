from trailcast.cli import app


def test_cli_app_importable() -> None:
    assert app is not None


def test_cli_app_is_typer_app() -> None:
    import typer

    assert isinstance(app, typer.Typer)
