import os
import shutil
from pathlib import Path

import click.testing
import pandas as pd
import pytest

from csv_parakeet import console


@pytest.fixture
def test_df() -> pd.DataFrame:
    return pd.DataFrame(data={"a": [0, 1, 2]})


def setup_function():
    os.makedirs("./testfiles", exist_ok=True)
    input_df = pd.DataFrame(data={"a": [0, 1, 2]})
    input_df.to_csv("./testfiles/test_input.csv", index=False)
    input_df.to_parquet("./testfiles/test_input.parquet", index=False)


def teardown_function():
    dirpath = Path("testfiles")
    if dirpath.exists():
        shutil.rmtree(dirpath)


def test_parakeet_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(console.parakeet)
    assert result.exit_code == 0


def test_c2p_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(
        console.c2p,
        args=["testfiles/test_input.csv", "testfiles/test_succeeds.parquet"],
    )
    assert result.exit_code == 0


def test_c2p_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.c2p, args=["testfiles/test_input.csv", "testfiles/test_output.parquet"]
    )
    saved_df = pd.read_parquet("testfiles/test_output.parquet")
    input_df = test_df
    pd.testing.assert_frame_equal(saved_df, input_df)


def test_p2c_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.p2c, args=["testfiles/test_input.parquet", "testfiles/test_output.csv"]
    )
    saved_df = pd.read_csv("testfiles/test_output.csv")
    input_df = test_df
    pd.testing.assert_frame_equal(saved_df, input_df)
