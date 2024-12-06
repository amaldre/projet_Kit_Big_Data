import sys
import os
import pytest
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from unittest.mock import patch, MagicMock
from utils.base_study import BaseStudy

def test_init():

    study = BaseStudy()

    assert study.dataframe is None
    assert study.default_values is None
    assert study.key is None
    assert study.iteration is None

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "date_column": pd.to_datetime(["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01"]),
        "numeric_column": [10, 50, 100, 150, 200],
    })

@patch("streamlit.date_input")
def test_set_date(mock_date_input, sample_dataframe):

    mock_date_input.side_effect = [
        pd.Timestamp("2021-01-01"),
        pd.Timestamp("2021-05-01"),
    ]

    study = BaseStudy()
    study.dataframe = sample_dataframe
    study.default_values = {"date_column": [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-05-01")]}
    study.key = "key"
    study.iteration = 1

    start_date, end_date = study._BaseStudy__set_date("date_column")

    mock_date_input.assert_any_call(
        "Start date",
        value=pd.Timestamp("2021-01-01"),
        min_value=pd.Timestamp("2021-01-01"),
        max_value=pd.Timestamp("2021-05-01"),
        key="start datekey1",
    )
    mock_date_input.assert_any_call(
        "End date",
        value=pd.Timestamp("2021-05-01"),
        min_value=pd.Timestamp("2021-01-01"),
        max_value=pd.Timestamp("2021-05-01"),
        key="end datekey1",
    )

    assert start_date == pd.Timestamp("2021-01-01")
    assert end_date == pd.Timestamp("2021-05-01")

@patch("streamlit.slider")
def test_create_slider_from_df(mock_slider):
    mock_slider.return_value = (50, 150)

    sample_dataframe = pd.DataFrame({
        "numeric_column": [10, 50, 100, 150, 200],
    })

    study = BaseStudy()
    study.dataframe = sample_dataframe
    study.default_values = {"numeric_column": [50, 150]}
    study.key = "key"
    study.iteration = 1

    result = study._BaseStudy__create_slider_from_df(sample_dataframe, "numeric_column")

    mock_slider.assert_called_once_with(
        label="Range for numeric_column",
        min_value=10,
        max_value=200,
        value=[50, 150],
        step=1,
        key="numeric_columnkey1",
    )

    assert result == (50, 150)