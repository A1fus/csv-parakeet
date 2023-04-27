import click
import pandas as pd

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.argument("file_in", nargs=1)
@click.argument("file_out", nargs=1)
def main(file_in, file_out):
    """Command line Parquet tool"""
    pd.read_csv(file_in).to_parquet(path=file_out, index=False)
