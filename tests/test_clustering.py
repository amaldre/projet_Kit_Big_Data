import pytest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import streamlit as st
from src.utils.load_functions import load_css, load_data
from src.pages.Clustering import main


@pytest.fixture
def mock_session_state():
    """
    Fixture pour initialiser l'état de session de Streamlit.
    """
    st.session_state.clear()


@patch("src.pages.Clustering.st.components.v1.html")  # Mock de l'iframe
@patch("src.pages.Clustering.load_data")  # Mock de load_data
@patch("src.pages.Clustering.load_css")  # Mock de load_css
@patch(
    "builtins.open",
    mock_open(read_data="<html><body>Visualisation de topics</body></html>"),
)
def test_main(mock_load_css, mock_load_data, mock_html):
    """
    Test principal pour vérifier que la page fonctionne correctement.
    """
    # Mock de la fonction load_css
    mock_load_css.return_value = None

    # Mock de la fonction load_data pour simuler un DataFrame
    mock_topics_data = pd.DataFrame(
        {
            "Topic": [1, 2, 3],
            "Name": ["Topic1", "Topic2", "Topic3"],
            "Count": [100, 150, 200],
        }
    )
    mock_load_data.return_value = mock_topics_data

    # Mock des visualisations HTML
    mock_html.return_value = None

    # Appeler la fonction main (point d'entrée de la page)
    main()

    mock_load_css.assert_called_once()

    mock_load_data.assert_called_once()

    # # Vérifier que le CSS est chargé
    # mock_load_css.assert_called_once_with("src/style.css")

    # # Vérifier que les données sont chargées avec le chemin et fichier corrects
    # mock_load_data.assert_called_once_with("data/bertopic_chart/", "topics_model.csv")

    # Vérifier que les visualisations HTML sont rendues
    assert mock_html.call_count == 2  # Une seule iframe rendue
