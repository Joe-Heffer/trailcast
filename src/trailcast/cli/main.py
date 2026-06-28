from __future__ import annotations

import typer

app = typer.Typer(
    name="trailcast",
    help="Trail conditions forecasting CLI for mountain biking stewards.",
    no_args_is_help=True,
)


@app.command()
def forecast(
    trail_name: str = typer.Argument(..., help="Name of the trail to forecast."),
    region: str | None = typer.Option(None, "--region", "-r", help="Region name."),
    hours: int = typer.Option(48, "--hours", "-h", help="Forecast horizon in hours."),
) -> None:
    """Generate a rideability forecast for a named trail."""
    raise NotImplementedError("Forecast engine not yet implemented.")


if __name__ == "__main__":
    app()
