import os
import shutil
from pathlib import Path

import click.testing
import pandas as pd

from parakeet import console


def setup_function():
    os.makedirs("./testfiles", exist_ok=True)
    pd.DataFrame(data={"a": [0, 1, 2]}).to_csv("./testfiles/test.csv")


def teardown_function():
    dirpath = Path("testfiles")
    if dirpath.exists():
        shutil.rmtree(dirpath)


def test_c2p_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(
        console.c2p, args=["testfiles/test.csv", "testfiles/test.parquet"]
    )
    assert result.exit_code == 0
