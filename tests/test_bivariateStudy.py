import sys
import os
import pytest
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from unittest.mock import patch, MagicMock
from utils.bivariateStudy import bivariateStudy

# TODO: Implement Test fct

def test_init_bivariate():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3]
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1"]
    axis_y_list = ["col1"]
    filters = ["col1"]
    axis_x = "col1"
    axis_y = "col1"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    assert study.dataframe.equals(df)
    assert study.axis_x_list == axis_x_list
    assert study.axis_y_list == axis_y_list
    assert study.filters == filters
    assert study.axis_x == axis_x
    assert study.axis_y == axis_y
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
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3], "col2": [4, 5, 6]
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1", "col2"]
    axis_y_list = ["col1", "col2"]
    filters = ["col1", "col2"]
    axis_x = "col1"
    axis_y = "col1"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    with patch("streamlit.selectbox") as mock_selectbox:
        mock_selectbox.side_effect = ["col1", "col2"]
        axis_x, axis_y = study._bivariateStudy__set_axis()

    assert axis_x == "col1"
    assert axis_y == "col2"

def test_create_slider_from_df():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5]
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1"]
    axis_y_list = ["col1"]
    filters = ["col1"]
    axis_x = "col1"
    axis_y = "col1"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = [1, 5]
        slider = study._bivariateStudy__create_slider_from_df(df, "col1")

    assert slider == [1, 5]

def test_set_date():
    df = pd.DataFrame(
        {
            "date_col": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"])
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["date_col"]
    axis_y_list = ["date_col"]
    filters = ["date_col"]
    axis_x = "date_col"
    axis_y = "date_col"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    with patch("streamlit.date_input") as mock_date_input:
        mock_date_input.side_effect = [datetime(2021, 1, 1), datetime(2021, 1, 3)]
        start_date, end_date = study._bivariateStudy__set_date("date_col")

    assert start_date == pd.to_datetime("2021-01-01")
    assert end_date == pd.to_datetime("2021-01-03")

def test_get_data_points():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [5, 4, 3, 2, 1],
            "filter_col": [10, 20, 30, 40, 50],
            "recipe_id": [101, 102, 103, 104, 105]
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1", "col2"]
    axis_y_list = ["col1", "col2"]
    filters = ["filter_col"]
    axis_x = "col1"
    axis_y = "col2"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    range_axis_x = [1, 5]
    range_axis_y = [1, 5]
    chosen_filters = ["filter_col"]
    range_filters = [[10, 50]]

    x, y, recipes_id = study.get_data_points(df, axis_x, axis_y, range_axis_x, range_axis_y, chosen_filters, range_filters)

    assert (x == np.array([1, 2, 3, 4, 5])).all()
    assert (y == np.array([5, 4, 3, 2, 1])).all()
    assert (recipes_id == np.array([101, 102, 103, 104, 105])).all()

def test_set_range_axis():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "date_col": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"])
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1", "date_col"]
    axis_y_list = ["col1", "date_col"]
    filters = ["col1", "date_col"]
    axis_x = "col1"
    axis_y = "col1"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    # Test for numeric column
    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = [1, 5]
        range_axis = study._bivariateStudy__set_range_axis("col1")
    assert range_axis == [1, 5]

    # Test for datetime column
    with patch("streamlit.date_input") as mock_date_input:
        mock_date_input.side_effect = [datetime(2021, 1, 1), datetime(2021, 1, 5)]
        range_axis = study._bivariateStudy__set_range_axis("date_col")
    assert range_axis == (pd.to_datetime("2021-01-01"), pd.to_datetime("2021-01-05"))

def test_filters():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [5, 4, 3, 2, 1],
            "filter_col1": [10, 20, 30, 40, 50],
            "filter_col2": [15, 25, 35, 45, 55]
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["col1", "col2"]
    axis_y_list = ["col1", "col2"]
    filters = ["filter_col1", "filter_col2"]
    axis_x = "col1"
    axis_y = "col2"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    with patch("streamlit.multiselect") as mock_multiselect, patch("streamlit.slider") as mock_slider:
        mock_multiselect.return_value = ["filter_col1"]
        mock_slider.return_value = [10, 50]
        chosen_filters, range_filters = study._bivariateStudy__filters(axis_x, axis_y)

    assert chosen_filters == ["filter_col1"]
    assert range_filters == [[10, 50]]
    
def test_draw_plot():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [5, 4, 3, 2, 1],
            "recipe_id": [101, 102, 103, 104, 105]
        }
    )
    plot_type = "scatter"
    axis_x_list = ["col1", "col2"]
    axis_y_list = ["col1", "col2"]
    filters = ["col1", "col2"]
    axis_x = "col1"
    axis_y = "col2"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    recipes_id = np.array([101, 102, 103, 104, 105])

    result = study._bivariateStudy__draw_plot(x, y, recipes_id)

    assert result == True

def test_display_graph():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [5, 4, 3, 2, 1],
            "filter_col": [10, 20, 30, 40, 50],
            "recipe_id": [101, 102, 103, 104, 105]
        }
    )
    plot_type = "scatter"
    axis_x_list = ["col1", "col2"]
    axis_y_list = ["col1", "col2"]
    filters = ["filter_col"]
    axis_x = "col1"
    axis_y = "col2"
    key = "test_key"

    study = bivariateStudy(key, df, plot_type, axis_x_list, axis_y_list, filters, axis_x, axis_y)

    result = study.display_graph(free=True)

    assert result == True
