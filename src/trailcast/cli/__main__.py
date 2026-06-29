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


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", help="Bind address."),
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on."),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload (development only)."),
) -> None:
    """Start the trailcast HTTP server.

    Requires the [server] extra:  pip install trailcast[server]
    """
    try:
        import uvicorn
    except ImportError:
        typer.echo("uvicorn is not installed. Run: pip install trailcast[server]", err=True)
        raise typer.Exit(code=1)

    uvicorn.run("trailcast.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
