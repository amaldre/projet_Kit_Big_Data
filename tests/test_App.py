import pytest
import streamlit as st
from streamlit import config
from unittest.mock import MagicMock, patch
from src.MangeTaData import main


@patch("src.MangeTaData.st")
@patch("src.MangeTaData.setup_logging")
@patch("src.MangeTaData.initialize_recipes_df")
@patch("src.MangeTaData.load_css")
def test_main(mock_st, mock_setup_logging, mock_initialize_recipes_df, mock_load_css):
    with patch("src.MangeTaData.st", mock_st):
        col1, col2, col3 = MagicMock(), MagicMock(), MagicMock()
        mock_st.columns.return_value = [col1, col2, col3]
        mock_st.set_page_config = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.image = MagicMock()
        main()
        mock_st.title.assert_called_once()
        mock_st.columns.assert_called_once_with([2, 3, 2])
        mock_st.title.assert_called_once_with("Mange ta main")
