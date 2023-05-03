import os
import shutil
from pathlib import Path

import click.testing
import pandas as pd
import pytest

from parakeet import console


@pytest.fixture
def test_df() -> pd.DataFrame:
    return pd.DataFrame(data={"a": [0, 1, 2]})


def setup_function():
    os.makedirs("./testfiles", exist_ok=True)
    input_df = pd.DataFrame(data={"a": [0, 1, 2]})
    input_df.to_csv("./testfiles/test.csv", index=False)


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


def test_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(console.c2p, args=["testfiles/test.csv", "testfiles/test.parquet"])
    saved_df = pd.read_parquet("testfiles/test.parquet")
    input_df = test_df
    pd.testing.assert_frame_equal(saved_df, input_df)
