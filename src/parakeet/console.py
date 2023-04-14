import click
from . import __version__

@click.command()
@click.version_option(version=__version__)
@click.argument("filename", nargs=1)
def main(filename):
    """Command line Parquet tool"""
    click.echo(f"filename: {filename}")

