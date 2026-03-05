"""Command-line interface for CacaoDocs."""
import http.server
import os
import socketserver
import sys
from pathlib import Path

import click


@click.group()
@click.version_option()
def cli():
    """CacaoDocs - Generate beautiful documentation from Python docstrings."""
    pass


@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="./docs",
    help="Output directory for generated documentation.",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(),
    default=None,
    help="Path to cacao.yaml configuration file.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output.",
)
def build(source: str, output: str, config: str | None, verbose: bool):
    """Build documentation from Python source files.

    SOURCE is the directory containing Python files to document.

    Examples:
        cacaodocs build ./src -o ./docs
        cacaodocs build C:\\Projects\\MyLib -o ./documentation
    """
    from .builder import build_docs
    from .config import load_config

    source_path = Path(source).resolve()
    output_path = Path(output).resolve()

    click.echo(f"Building documentation from: {source_path}")
    click.echo(f"Output directory: {output_path}")

    # Load configuration
    cfg = load_config(config)
    if verbose:
        cfg["verbose"] = True

    try:
        json_data = build_docs(source_path, output_path, cfg)

        # Print summary
        num_modules = len(json_data.get("modules", []))
        num_classes = len(json_data.get("classes", []))
        num_functions = len(json_data.get("functions", []))
        num_pages = len(json_data.get("pages", []))

        click.echo()
        click.echo(click.style("Documentation built successfully!", fg="green", bold=True))
        click.echo()
        click.echo(f"  Modules:   {num_modules}")
        click.echo(f"  Classes:   {num_classes}")
        click.echo(f"  Functions: {num_functions}")
        click.echo(f"  Pages:     {num_pages}")
        click.echo()
        click.echo(f"Open {output_path / 'index.html'} in your browser to view.")

    except FileNotFoundError as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"Error building documentation: {e}", fg="red"), err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("directory", type=click.Path(exists=True), default="./docs")
@click.option(
    "-p",
    "--port",
    type=int,
    default=8000,
    help="Port to serve on.",
)
def serve(directory: str, port: int):
    """Serve generated documentation locally.

    DIRECTORY is the path to the generated docs (default: ./docs).

    Examples:
        cacaodocs serve
        cacaodocs serve ./my-docs -p 3000
    """
    directory = Path(directory).resolve()

    if not (directory / "index.html").exists():
        click.echo(
            click.style(
                f"Error: No index.html found in {directory}. Run 'cacaodocs build' first.",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)

    os.chdir(directory)

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        click.echo(f"Serving documentation at http://localhost:{port}")
        click.echo("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\nServer stopped.")


@cli.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="cacao.yaml",
    help="Output path for configuration file.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite existing configuration file.",
)
def init(output: str, force: bool):
    """Create a default cacao.yaml configuration file.

    Examples:
        cacaodocs init
        cacaodocs init -o myconfig.yaml
    """
    from .config import create_default_config

    output_path = Path(output)

    if output_path.exists() and not force:
        click.echo(
            click.style(
                f"Error: {output_path} already exists. Use --force to overwrite.",
                fg="red",
            ),
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
