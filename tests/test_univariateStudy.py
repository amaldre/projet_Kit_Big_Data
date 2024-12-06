import sys
import os
import pytest
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from unittest.mock import patch, MagicMock
from utils.univariate_study import univariate_study


def test_init_univariate():
    df = pd.DataFrame({"col1": [1, 2, 3]})
    plot_type = "plot_type"
    axis_x_list = ["col1"]
    filters = ["col1"]
    axis_x = "col1"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    assert study.dataframe.equals(df)
    assert study.axis_x_list == axis_x_list
    assert study.filters == filters
    assert study.axis_x == axis_x
    assert study.key == key
    assert study.delete is False
    assert study.plot_type == plot_type
    assert study.first_draw is True
    assert study.name == key
    assert study.default_values is None
    assert study.default_values_save is None
    assert study.chosen_filters is None
    assert study.range_filters is None
    assert study.iteration == 1
    assert study.log_axis_x is False
    assert study.log_axis_y is False


def test_set_axis_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
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

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    study._univariate_study__set_axis()
    assert study.axis_x == axis_x


def test_set_date_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "date_col": pd.to_datetime(
                ["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01"]
            ),
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["date_col"]
    filters = ["date_col"]
    axis_x = "date_col"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.date_input") as mock_date_input:
        mock_date_input.side_effect = [datetime(2021, 1, 1), datetime(2021, 5, 1)]
        start_date, end_date = study._univariate_study__set_date(axis_x)

    assert start_date == pd.to_datetime("2021-01-01")
    assert end_date == pd.to_datetime("2021-05-01")


def test_set_number_ingredients_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "ingredients": [
                "ing1, ing2",
                "ing3, ing4",
                "ing5, ing6",
                "ing7, ing8",
                "ing9, ing10",
            ],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["ingredients"]
    filters = ["ingredients"]
    axis_x = "ingredients"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = (1, 5)
        min_ingredients, max_ingredients = (
            study._univariate_study__set_number_ingredients(axis_x)
        )

    assert min_ingredients == 1
    assert max_ingredients == 5


def test_create_slider_from_df_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "numeric_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["numeric_col"]
    filters = ["numeric_col"]
    axis_x = "numeric_col"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = (10, 50)
        slider_range = study._univariate_study__create_slider_from_df(df, axis_x)

    assert slider_range == (10, 50)


def test_set_range_axis_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "numeric_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["numeric_col"]
    filters = ["numeric_col"]
    axis_x = "numeric_col"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = (10, 50)
        range_axis = study._univariate_study__set_range_axis(axis_x)

    assert range_axis == (10, 50)


def test_get_data_points_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "filter_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["filter_col"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    range_axis_x = (2, 4)
    chosen_filters = ["filter_col"]
    range_filters = [(15, 35)]

    x_values, ids = study.get_data_points(
        df, axis_x, range_axis_x, chosen_filters, range_filters
    )

    expected_df = df[
        (df[axis_x] >= range_axis_x[0])
        & (df[axis_x] <= range_axis_x[1])
        & (df["filter_col"] >= range_filters[0][0])
        & (df["filter_col"] <= range_filters[0][1])
    ]

    assert list(x_values) == list(expected_df[axis_x])
    assert list(ids) == list(expected_df["recipe_id"])


def test_get_data_points_ingredients_univariate():
    df = pd.DataFrame(
        {
            "axis_x": [
                ["ingredient1", "ingredient2"],
                ["ingredient1"],
                ["ingredient3"],
            ],
            "filter1": [5, 10, 15],
            "filter2": [20, 25, 30],
            "recipe_id": [101, 102, 103],
        }
    )

    univariate_study = univariate_study(
        key="test_key",
        dataframe=df,
        plot_type="bar",
    )

    axis_x = "axis_x"
    range_axis_x = 3
    chosen_filters = ["filter1", "filter2"]
    range_filters = [(5, 15), (20, 30)]

    list_elts, count_elts, recipe_ids = univariate_study.get_data_points_ingredients(
        df, axis_x, range_axis_x, chosen_filters, range_filters
    )

    assert list_elts == ["ingredient1", "ingredient2", "ingredient3"]
    assert count_elts == [2, 1, 1]
    assert (recipe_ids == [101, 102, 103]).all()


def test_filters_univariate():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "numeric_col": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["numeric_col"]
    filters = ["numeric_col"]
    axis_x = "numeric_col"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)

    with patch("streamlit.multiselect") as mock_multiselect, patch(
        "streamlit.slider"
    ) as mock_slider:
        mock_multiselect.return_value = ["numeric_col"]
        mock_slider.return_value = (10, 50)
        chosen_filters, range_filters = study._univariate_study__filters(axis_x)

    assert chosen_filters == ["numeric_col"]
    assert range_filters == [(10, 50)]


def test_graph_normal():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    x = df[axis_x].values
    result = study.graph_normal(x)
    assert result is True


def test_graph_boxplot():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    x = df[axis_x].values
    result = study.graph_boxplot(x)
    assert result is True


def test_graph_density():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    x = df[axis_x].values
    result = study.graph_density(x)
    assert result is True


def test_graph_histogram():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    x = df[axis_x].values
    result = study.graph_histogram(x)
    assert result is True


def test_graph_bar_elts():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "bar_ingredients"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"

    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    nb_elts_display = ["ingredient1", "ingredient2", "ingredient3"]
    count_elts = [10, 20, 30]
    result = study.graph_bar_elts(nb_elts_display, count_elts)
    assert result is True


def test_draw_graph():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "comment_count": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "boxplot"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"
    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    x = df[axis_x].values
    y = None
    recipes_id = df["recipe_id"].values
    result = study._univariate_study__draw_graph(x, y, recipes_id)
    assert result is True


def test_axis_graph():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "plot_type"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"
    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    fig, ax = plt.subplots()
    result = study.axis_graph(fig, ax)
    assert result is True


def test_display_graph():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "comment_count": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "boxplot"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"
    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    result = study.display_graph()
    assert result is True


def test_display_graph_with_params():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "comment_count": [10, 20, 30, 40, 50],
        }
    )
    plot_type = "boxplot"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"
    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    result = study.display_graph(free=True, explanation="some explanation")
    assert result is True


def test_save_graph():
    df = pd.DataFrame(
        {
            "recipe_id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
        }
    )
    plot_type = "histogram"
    axis_x_list = ["axis_x"]
    filters = ["axis_x"]
    axis_x = "axis_x"
    key = "test_key"
    study = univariate_study(key, df, plot_type, axis_x_list, filters, axis_x)
    with patch("streamlit.write") as mock_write:
        study.save_graph()
    mock_write.assert_called_once()
