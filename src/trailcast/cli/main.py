from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer(
    name="trailcast",
    help="Trail conditions forecasting CLI for mountain biking stewards.",
    no_args_is_help=True,
)


@app.command()
def forecast(
    trail_name: str = typer.Argument(..., help="Name of the trail to forecast."),
    gpx: Path | None = typer.Option(
        None,
        "--gpx",
        "-g",
        help="Path to a GPX file containing the trail polyline.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    region: str | None = typer.Option(None, "--region", "-r", help="Region name."),
    hours: int = typer.Option(48, "--hours", "-h", help="Forecast horizon in hours."),
) -> None:
    """Generate a rideability forecast for a named trail.

    Pass --gpx to supply a GPS polyline directly, or omit it to look up the
    trail from the local registry at ~/.trailcast/trails.json.
    """
    raise NotImplementedError("Forecast engine not yet implemented.")


if __name__ == "__main__":
    app()
