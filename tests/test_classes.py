# tests/test_classes.py

import sys
import os
import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
from utils.classes import bivariateStudy
from utils.univariateStudy import univariateStudy


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


# def test_study_get_data_points():
#     # Créer un DataFrame d'exemple
#     df = pd.DataFrame(
#         {
#             "id": [1, 2, 3, 4, 5],
#             "axis_x": [1, 2, 3, 4, 5],
#             "axis_y": [5, 4, 3, 2, 1],
#             "filter_col": [10, 20, 30, 40, 50],
#         }
#     )
#     axis_x_list = ["axis_x"]
#     axis_y_list = ["axis_y"]
#     filters = ["filter_col"]
#     key = "test_key"

#     study = bivariateStudy(key, df, "plot_type", axis_x_list, axis_y_list, filters)

#     axis_x = "axis_x"
#     axis_y = "axis_y"
#     range_axis_x = (2, 4)
#     range_axis_y = (2, 4)
#     chosen_filters = ["filter_col"]
#     range_filters = [(15, 35)]

#     x_values, y_values, ids = study.get_data_points(
#         df, axis_x, axis_y, range_axis_x, range_axis_y, chosen_filters, range_filters
#     )

#     # DataFrame attendu après filtrage
#     expected_df = df[
#         (df[axis_x] >= range_axis_x[0])
#         & (df[axis_x] <= range_axis_x[1])
#         & (df[axis_y] >= range_axis_y[0])
#         & (df[axis_y] <= range_axis_y[1])
#         & (df["filter_col"] >= range_filters[0][0])
#         & (df["filter_col"] <= range_filters[0][1])
#     ]

#     assert list(x_values) == list(expected_df[axis_x])
#     assert list(y_values) == list(expected_df[axis_y])
#     assert list(ids) == list(expected_df["id"])

# univariateStudy
def test_univariate_study_init():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame({"col1": [1, 2, 3]})
    plot_type = "plot_type"
    axis_x_list = ["col1"]
    filters = ["col1"]
    axis_x = "col1"
    key = "test_key"

    study = univariateStudy(key, df, plot_type, axis_x_list, filters, axis_x)

    assert study.dataframe.equals(df)
    assert study.axis_x_list == axis_x_list
    assert study.filters == filters
    assert study.axis_x == axis_x
    assert study.key == key
    assert study.delete == False
    assert study.plot_type == plot_type
    assert study.first_draw == True
    assert study.name == key
    assert study.default_values == None
    assert study.default_values_save == None
    assert study.chosen_filters == None
    assert study.range_filters == None
    assert study.iteration == 1
    assert study.log_axis_x == False
    assert study.log_axis_y == False


def test_set_axis():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "axis_y": [5, 4, 3, 2, 1],
            "filter_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["filter_col"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariateStudy(key, df, plot_type, axis_x_list, filters, axis_x)

    study._univariateStudy__set_axis()

    assert study.axis_x == axis_x

def test_set_date():
    # Créer un DataFrame d'exemple avec des dates
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "date_col": pd.to_datetime(["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01"]),
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["date_col"]
    filters = ["date_col"]
    axis_x = "date_col"
    key = "test_key"

    study = univariateStudy(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.date_input") as mock_date_input:
        mock_date_input.side_effect = [datetime(2021, 1, 1), datetime(2021, 5, 1)]
        start_date, end_date = study._univariateStudy__set_date(axis_x)

    assert start_date == pd.to_datetime("2021-01-01")
    assert end_date == pd.to_datetime("2021-05-01")

def test_set_number_ingredients():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "ingredients": ["ing1, ing2", "ing3, ing4", "ing5, ing6", "ing7, ing8", "ing9, ing10"],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["ingredients"]
    filters = ["ingredients"]
    axis_x = "ingredients"
    key = "test_key"

    study = univariateStudy(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = (1, 5)
        min_ingredients, max_ingredients = study._univariateStudy__set_number_ingredients(axis_x)

    assert min_ingredients == 1
    assert max_ingredients == 5

def test_create_slider_from_df():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "numeric_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["numeric_col"]
    filters = ["numeric_col"]
    axis_x = "numeric_col"
    key = "test_key"

    study = univariateStudy(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = (10, 50)
        slider_range = study._univariateStudy__create_slider_from_df(df, axis_x)

    assert slider_range == (10, 50)

