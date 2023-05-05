import click
import pandas as pd

from . import __version__


@click.group()
@click.version_option(version=__version__)
def parakeet() -> None:
    return None  # pragma: no cover


@parakeet.command()
@click.argument("file_in", type=click.Path(exists=True), nargs=1)
@click.argument("file_out", type=click.Path(), nargs=1)
def c2p(file_in, file_out):
    """Convert a CSV file to parquet format"""
    pd.read_csv(file_in).to_parquet(path=file_out, index=False)


@parakeet.command()
@click.argument("file_in", type=click.Path(exists=True), nargs=1)
@click.argument("file_out", type=click.Path(), nargs=1)
def p2c(file_in, file_out):
    """Convert a parqet file to CSV format"""
    pd.read_parquet(file_in).to_csv(path_or_buf=file_out, index=False)
