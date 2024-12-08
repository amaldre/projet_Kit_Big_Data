import unittest
from unittest import mock
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import streamlit as st

from src.pages.4_Preprocessing import main

@patch('streamlit.title')
@patch('streamlit.write')
@patch('streamlit.success')
@patch('streamlit.error')
@patch('streamlit.header')
@patch("src.pages.4_Preprocessing.st.components.v1.html")
@patch("src.pages.4_Preprocessing.load_data")
@patch("src.pages.4_Preprocessing.load_css")
@patch("builtins.open", mock_open(read_data="<html><body>Visualisation de topics</body></html>"))

def test_main(
    mock_load_css, mock_load_data, mock_html,
    mock_st_error, mock_st_success, mock_st_write, mock_st_title, mock_st_header
):

    mock_load_css.return_value = None

    mock_topics_data = pd.DataFrame({
        "Topic": [1, 2, 3],
        "Name": ["Topic1", "Topic2", "Topic3"],
        "Count": [100, 150, 200],
    })
    mock_load_data.return_value = mock_topics_data

    mock_html.return_value = None

    main()

    assert mock_st_title.call_count == 15
    mock_st_header.assert_called_once()
    

    assert mock_html.call_count == 1