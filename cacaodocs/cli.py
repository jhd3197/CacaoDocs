"""Command-line interface for CacaoDocs."""
import subprocess
import sys
from pathlib import Path

import click


@click.group()
@click.version_option()
def cli():
    """CacaoDocs - Generate documentation powered by Cacao."""
    pass


@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default="./docs", help="Output directory.")
@click.option("-c", "--config", type=click.Path(), default=None, help="Path to cacao.yaml.")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
def build(source: str, output: str, config: str | None, verbose: bool):
    """Build documentation from Python source files.

    SOURCE is the directory containing Python files to document.

    Examples:
        cacaodocs build ./src -o ./docs
        cacaodocs build ./my-project
    """
    from .builder import build_docs
    from .config import load_config

    source_path = Path(source).resolve()
    output_path = Path(output).resolve()

    click.echo(f"Scanning: {source_path}")

    cfg = load_config(config)
    if verbose:
        cfg["verbose"] = True

    try:
        json_data = build_docs(source_path, output_path, cfg)

        num_modules = len(json_data.get("modules", []))
        num_classes = len(json_data.get("classes", []))
        num_functions = len(json_data.get("functions", []))
        num_api = len(json_data.get("api_endpoints", []))
        num_pages = len(json_data.get("pages", []))

        click.echo()
        click.echo(click.style("Documentation built!", fg="green", bold=True))
        click.echo()
        click.echo(f"  Modules:       {num_modules}")
        click.echo(f"  Classes:       {num_classes}")
        click.echo(f"  Functions:     {num_functions}")
        if num_api:
            click.echo(f"  API Endpoints: {num_api}")
        click.echo(f"  Pages:         {num_pages}")
        click.echo()
        click.echo(f"  Output: {output_path / 'app.py'}")
        click.echo()
        click.echo(f"Run with: cacaodocs serve {output_path}")

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("directory", type=click.Path(exists=True), default="./docs")
@click.option("-p", "--port", type=int, default=1502, help="Port to serve on.")
@click.option("--host", type=str, default="127.0.0.1", help="Host to bind to.")
def serve(directory: str, port: int, host: str):
    """Serve generated documentation using Cacao.

    DIRECTORY is the path to the generated docs (default: ./docs).

    Examples:
        cacaodocs serve
        cacaodocs serve ./my-docs -p 3000
    """
    directory = Path(directory).resolve()
    app_file = directory / "app.py"

    if not app_file.exists():
        click.echo(
            click.style(
                f"Error: No app.py found in {directory}. Run 'cacaodocs build' first.",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)

    click.echo(f"Serving docs at http://{host}:{port}")
    click.echo("Press Ctrl+C to stop.")

    try:
        subprocess.run(
            ["cacao", "run", str(app_file), "--port", str(port)],
            check=True,
        )
    except FileNotFoundError:
        click.echo(
            click.style("Error: Cacao not found. Install it: pip install cacao", fg="red"),
            err=True,
        )
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nStopped.")


@cli.command()
@click.option("-o", "--output", type=click.Path(), default="cacao.yaml", help="Output path.")
@click.option("-f", "--force", is_flag=True, help="Overwrite existing file.")
def init(output: str, force: bool):
    """Create a default cacao.yaml configuration file."""
    from .config import create_default_config

    output_path = Path(output)

    if output_path.exists() and not force:
        click.echo(
            click.style(f"Error: {output_path} already exists. Use --force to overwrite.", fg="red"),
            err=True,
        )
        sys.exit(1)

    create_default_config(output_path)
    click.echo(click.style(f"Created {output_path}", fg="green"))


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
