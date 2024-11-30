# tests/test_classes.py

import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.classes import bivariateStudy


def test_study_init():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame({"col1": [1, 2, 3]})
    axis_x_list = ["col1"]
    axis_y_list = ["col1"]
    filters = ["col1"]
    key = "test_key"

    study = bivariateStudy(key, df, "plot_type", axis_x_list, axis_y_list, filters)

    assert study.dataframe.equals(df)
    assert study.axis_x_list == axis_x_list
    assert study.axis_y_list == axis_y_list
    assert study.filters == filters
    assert study.key == key
    assert study.delete == False


def test_study_get_data_points():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "axis_y": [5, 4, 3, 2, 1],
            "filter_col": [10, 20, 30, 40, 50],
        }
    )
    axis_x_list = ["axis_x"]
    axis_y_list = ["axis_y"]
    filters = ["filter_col"]
    key = "test_key"

    study = bivariateStudy(key, df, "plot_type", axis_x_list, axis_y_list, filters)

    axis_x = "axis_x"
    axis_y = "axis_y"
    range_axis_x = (2, 4)
    range_axis_y = (2, 4)
    chosen_filters = ["filter_col"]
    range_filters = [(15, 35)]

    x_values, y_values, ids = study.get_data_points(
        df, axis_x, axis_y, range_axis_x, range_axis_y, chosen_filters, range_filters
    )

    # DataFrame attendu après filtrage
    expected_df = df[
        (df[axis_x] >= range_axis_x[0])
        & (df[axis_x] <= range_axis_x[1])
        & (df[axis_y] >= range_axis_y[0])
        & (df[axis_y] <= range_axis_y[1])
        & (df["filter_col"] >= range_filters[0][0])
        & (df["filter_col"] <= range_filters[0][1])
    ]

    assert list(x_values) == list(expected_df[axis_x])
    assert list(y_values) == list(expected_df[axis_y])
    assert list(ids) == list(expected_df["id"])
