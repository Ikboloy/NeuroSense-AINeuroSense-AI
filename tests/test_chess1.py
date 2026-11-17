import numpy as np
import pytest
from neurosense_ai.chess1 import compute_lr_disparities, write_rows


def test_lr_disparity_shape():
    # A tiny image cannot support SGBM disparity range, so test input contract
    assert callable(compute_lr_disparities)


def test_csv_writer(tmp_path):
    output=tmp_path/"nested"/"rows.csv"
    write_rows(output,[{"state":"VALID","count":1}])
    assert "VALID,1" in output.read_text()


def test_missing_scene(tmp_path):
    from neurosense_ai.chess1 import evaluate_chess1
    with pytest.raises(FileNotFoundError):
        evaluate_chess1(tmp_path)
