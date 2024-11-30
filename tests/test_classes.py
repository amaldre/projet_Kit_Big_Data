# tests/test_classes.py

import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.classes import Study


def test_study_init():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame({"col1": [1, 2, 3]})
    axis_x_list = ["col1"]
    axis_y_list = ["col1"]
    filters = ["col1"]
    key = "test_key"

    study = Study(df, axis_x_list, axis_y_list, filters, key)

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

    study = Study(df, axis_x_list, axis_y_list, filters, key)

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


def test_study_display_graph():
    # Mock des fonctions Streamlit
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "axis_x": [1, 2, 3],
            "axis_y": [3, 2, 1],
            "count_total": [100, 200, 300],
        }
    )
    axis_x_list = ["axis_x"]
    axis_y_list = ["axis_y"]
    filters = []
    key = "test_key"

    study = Study(df, axis_x_list, axis_y_list, filters, key)

    with patch("streamlit.expander"), patch(
        "streamlit.selectbox", side_effect=["axis_x", "axis_y"]
    ), patch("streamlit.slider", return_value=(1, 3)), patch("streamlit.form"), patch(
        "streamlit.form_submit_button", side_effect=[True, False]
    ), patch(
        "streamlit.columns", return_value=[MagicMock(), MagicMock(), MagicMock()]
    ), patch(
        "streamlit.pyplot"
    ), patch(
        "matplotlib.pyplot.subplots", return_value=(MagicMock(), MagicMock())
    ), patch(
        "streamlit.dataframe"
    ), patch(
        "streamlit.write"
    ), patch(
        "streamlit.checkbox", return_value=False
    ):

        # Exécuter la méthode display_graph
        study.display_graph()
        # Vous pouvez ajouter des assertions supplémentaires si nécessaire
