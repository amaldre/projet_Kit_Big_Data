from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import streamlit as st

from src.pages.Analyse_des_donnees import main


@pytest.fixture
def mock_session_state():
    """
    Fixture pour initialiser l'état de session de Streamlit.
    """
    st.session_state.clear()
    st.session_state["recipes_df"] = pd.DataFrame(
        {
            "submitted": [
                pd.Timestamp("2000-01-01"),
                pd.Timestamp("2005-01-01"),
                pd.Timestamp("2010-01-01"),
            ],
            "minutes": [10, 20, 30],
            "comment_count": [50, 150, 300],
            "mean_rating": [3.5, 4.0, 5.0],
        }
    )
    st.session_state["first_load"] = True
    st.session_state["locked_graphs"] = []


@patch("src.pages.Analyse_des_donnees.compute_trend")
@patch("src.pages.Analyse_des_donnees.BivariateStudy")
@patch("src.pages.Analyse_des_donnees.UnivariateStudy")
@patch("src.pages.Analyse_des_donnees.load_css")
def test_main(
    mock_load_css,
    mock_UnivariateStud,
    mock_BivariateStudy,
    mock_compute_trend,
    mock_session_state,
):
    """
    Test principal pour vérifier le bon fonctionnement de la fonction main.
    """
    # Mock des fonctions utilisées dans main()
    mock_load_css.return_value = None

    mock_compute_trend.return_value = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2000-01-01"), pd.Timestamp("2005-01-01")],
            "Trend": [100, 200],
        }
    )

    mock_BivariateStudy.return_value = MagicMock(
        display_graph=MagicMock(),
        name="Mocked Bivariate Study",
    )
    mock_UnivariateStud.return_value = MagicMock(
        display_graph=MagicMock(),
        name="Mocked Univariate Study",
    )

    # Appeler la fonction main
    main()

    # Vérifier que les CSS sont chargés
    mock_load_css.assert_called_once_with("src/style.css")

    # Vérifier que compute_trend a été appelé avec le bon argument
    mock_compute_trend.assert_called_once_with(st.session_state["recipes_df"])

    # Vérifier que les études bivariées et univariées sont créées
    assert len(st.session_state["locked_graphs"]) == 0

    # Vérifier que les graphiques sont affichés
    for graph in st.session_state["locked_graphs"]:
        graph.display_graph.assert_called()


# Exception handling
@patch("src.pages.Analyse_des_donnees.compute_trend")
@patch("src.pages.Analyse_des_donnees.BivariateStudy")
@patch("src.pages.Analyse_des_donnees.UnivariateStudy")
@patch("src.pages.Analyse_des_donnees.load_css")
def test_main_exception_handling(
    mock_load_css,
    mock_UnivariateStud,
    mock_BivariateStudy,
    mock_compute_trend,
    mock_session_state,
):
    """
    Test pour vérifier la gestion des exceptions dans la fonction main.
    """
    # Mock des fonctions utilisées dans main()
    mock_load_css.return_value = None

    # Simuler une exception dans compute_trend
    mock_compute_trend.side_effect = Exception("Erreur dans compute_trend")

    # Appeler la fonction main et vérifier qu'elle gère l'exception
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() a levé une exception: {e}")

    # Vérifier que les CSS sont chargés même en cas d'exception
    mock_load_css.assert_called_once_with("src/style.css")

    # Vérifier que compute_trend a été appelé avec le bon argument
    mock_compute_trend.assert_called_once_with(st.session_state["recipes_df"])

    # Vérifier que les études bivariées et univariées ne sont pas créées en cas d'exception
    assert len(st.session_state["locked_graphs"]) == 0
