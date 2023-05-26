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
    input_df_2 = pd.DataFrame(data={"a": [4, 5, 6]})
    input_df.to_csv("./testfiles/test_input.csv", index=False)
    input_df_2.to_csv("./testfiles/test_input_2.csv", index=False)
    input_df.to_parquet("./testfiles/test_input.parquet", index=False)
    input_df_2.to_parquet("./testfiles/test_input_2.parquet", index=False)
    pd.concat([input_df, input_df_2], ignore_index=True).to_parquet(
        "./testfiles/expected_output_concat.parquet", index=False
    )
    pd.concat([input_df, input_df_2], ignore_index=True).to_csv(
        "./testfiles/expected_output_concat.csv", index=False
    )


def teardown_function():
    dirpath = Path("testfiles")
    if dirpath.exists():
        shutil.rmtree(dirpath)


def test_c2p_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.c2p, args=["testfiles/test_input.csv", "testfiles/test_output.parquet"]
    )
    saved_df = pd.read_parquet("testfiles/test_output.parquet")
    input_df = test_df
    pd.testing.assert_frame_equal(saved_df, input_df)


def test_c2p_multifile_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.c2p,
        args=[
            "testfiles/test_input.csv",
            "testfiles/test_input_2.csv",
            "testfiles/test_output_concat.parquet",
        ],
    )
    saved_df = pd.read_parquet("testfiles/test_output_concat.parquet")
    expected_df = pd.read_parquet("testfiles/expected_output_concat.parquet")
    pd.testing.assert_frame_equal(saved_df, expected_df)


def test_p2c_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.p2c, args=["testfiles/test_input.parquet", "testfiles/test_output.csv"]
    )
    saved_df = pd.read_csv("testfiles/test_output.csv")
    input_df = test_df
    pd.testing.assert_frame_equal(saved_df, input_df)


def test_p2c_multifile_output_correct(test_df):
    runner = click.testing.CliRunner()
    runner.invoke(
        console.p2c,
        args=[
            "testfiles/test_input.parquet",
            "testfiles/test_input_2.parquet",
            "testfiles/test_output_concat.csv",
        ],
    )
    saved_df = pd.read_csv("testfiles/test_output_concat.csv")
    expected_df = pd.read_csv("testfiles/expected_output_concat.csv")
    pd.testing.assert_frame_equal(saved_df, expected_df)
