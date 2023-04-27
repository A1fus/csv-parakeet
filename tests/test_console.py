import click.testing
from parakeet import console
import shutil
from pathlib import Path
import os
import pandas as pd


def setup_function():
    os.makedirs("./testfiles",exist_ok=True)
    pd.DataFrame(data={"a":[0,1,2]}).to_csv("./testfiles/test.csv")


def teardown_function():
    dirpath = Path("testfiles")
    if dirpath.exists(): 
      shutil.rmtree(dirpath)


def test_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(console.main, args=["test.csv","testfiles/test.parquet"])
    assert result.exit_code == 0
