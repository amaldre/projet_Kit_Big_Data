# tests/test_classes.py

import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.classes import bivariateStudy
from utils.classes import AdvancedStudy


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

# AdvancedStudy

def test_advancedstudy_init():
    # Créer un Dataframe d'exemple
    df = pd.DataFrame({"col1": [1, 2, 3]})
    axis_x_list = ["col1"]
    filters = ["col1"]
    key = "test_key"

    advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

    assert advanced_study.dataframe.equals(df)
    assert advanced_study.axis_x_list == axis_x_list
    assert advanced_study.filters == filters
    assert advanced_study.key == key
    assert advanced_study.delete == False
    
def test_advancedstudy_set_axis():
    df = pd.DataFrame()
    axis_x_list = ["axis_x1", "axis_x2"]
    filters = []
    key = "test_key"

    advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

    # Mock Streamlit selectbox
    streamlit_mock = MagicMock()
    streamlit_mock.selectbox.return_value = "axis_x1"

    # Replace the Streamlit function with the mock
    with MagicMock() as mock_streamlit:
        mock_streamlit.selectbox = streamlit_mock.selectbox
        result = advanced_study.__set_axis()

    assert result == "axis_x1"
    streamlit_mock.selectbox.assert_called_once_with(
        label=f"graph {key}",
        options=axis_x_list,
        key=f"{key}_axis_x"
    )

def test_advancedstudy_get_data_points():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "filter_col": [10, 20, 30, 40, 50],
        }
    )
    axis_x_list = ["axis_x"]
    filters = ["filter_col"]
    key = "test_key"

    advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

    axis_x = "axis_x"
    range_axis_x = (2, 4)
    chosen_filters = ["filter_col"]
    range_filters = [(15, 35)]

    x_values, ids = advanced_study.get_data_points(
        df, axis_x, range_axis_x, chosen_filters, range_filters
    )

    # DataFrame attendu après filtrage
    expected_df = df[
        (df[axis_x] >= range_axis_x[0])
        & (df[axis_x] <= range_axis_x[1])
        & (df["filter_col"] >= range_filters[0][0])
        & (df["filter_col"] <= range_filters[0][1])
    ]

    assert list(x_values) == list(expected_df[axis_x])
    assert list(ids) == list(expected_df["id"])

def test_get_data_points_ingredients():
    # Créer un Dataframe d'exemple
    df = pd.DataFrame({
        "recipe_id": ["a", "b", "c"],
        "ingredients_replaced": ["ing1", "ing2", "ing3"]
    })
    axis_x_list = ["ingredients_replaced"]
    filters = []
    key = "test_key"

    advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

    result = advanced_study.get_data_points_ingredients(df)

    assert list(result) == ["a", "b", "c"]

def test_avdancedstudy_filters():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "filter1": [10, 20, 30],
        "filter2": [40, 50, 60]
    })
    axis_x_list = ["col1"]
    filters = ["filter1", "filter2"]
    key = "test_key"

    advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

    # Mock Streamlit sidebar components
    mock_sidebar = MagicMock()
    mock_sidebar.multiselect.return_value = ["filter1"]
    mock_sidebar.slider.return_value = (15, 25)

    # Replace Streamlit's sidebar methods with mocks
    with MagicMock() as mock_streamlit:
        mock_streamlit.sidebar = mock_sidebar
        chosen_filters, range_filters = advanced_study.__filters("col1")

    assert chosen_filters == ["filter1"]
    assert range_filters == [(15, 25)]
    mock_sidebar.multiselect.assert_called_once_with(
        label=f"filtre pour le graph {key}",
        options=["filter1", "filter2"],
        key=f"{key}_chosen_filters"
    )
    mock_sidebar.slider.assert_called_once_with(
        "filter1", min_value=10, max_value=30, value=(10, 30), key=f"{key}_range_filter1"
    )