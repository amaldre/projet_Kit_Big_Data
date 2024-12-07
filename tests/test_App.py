import pytest
import streamlit as st
from streamlit import config
from unittest.mock import MagicMock, patch
from src.App import main

@patch("src.App.st")
@patch("src.App.setup_logging")
@patch("src.App.initialize_recipes_df")
@patch("src.App.load_css")
def test_main(mock_st, mock_setup_logging, mock_initialize_recipes_df, mock_load_css):
    with patch("src.App.st",mock_st):
        mock_st.set_page_config = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        main()
        mock_st.title.assert_called_once()