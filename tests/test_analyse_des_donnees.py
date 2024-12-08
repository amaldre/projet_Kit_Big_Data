from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import streamlit as st

# from src.pages.1_Analyse_des_donnees import main
import importlib

# Charger dynamiquement le module
main = importlib.import_module("src.pages.1_Analyse_des_donnees").main


@pytest.fixture
def mock_session_state():
    """
    Fixture pour initialiser le session_state mocké.
    """
    session_state = {
        "recipes_df": pd.DataFrame(
            {
                "submitted": pd.date_range(start="1999-01-01", periods=100, freq="YE"),
                "comment_count": range(100),
                "mean_rating": [4.5] * 100,
                "minutes": [30] * 100,
            }
        ),
        "first_load": True,
        "locked_graphs": {},
    }
    return session_state


@patch("src.pages.1_Analyse_des_donnees.st")
@patch("src.pages.1_Analyse_des_donnees.load_css")
@patch("src.pages.1_Analyse_des_donnees.compute_trend")
@patch("src.pages.1_Analyse_des_donnees.BivariateStudy")
@patch("src.pages.1_Analyse_des_donnees.UnivariateStudy")
def test_main(
    mock_univariate_study,
    mock_bivariate_study,
    mock_compute_trend,
    mock_load_css,
    mock_st,
):
    """
    Test principal pour vérifier que la fonction main s'exécute correctement.
    """
    # Mock des fonctions et classes
    mock_load_css.return_value = None

    mock_compute_trend.return_value = pd.DataFrame(
        {
            "Date": pd.date_range(start="2000-01-01", periods=20, freq="YE"),
            "Trend": range(20),
        }
    )

    mock_bivariate_instance = MagicMock()
    mock_bivariate_study.return_value = mock_bivariate_instance

    mock_univariate_instance = MagicMock()
    mock_univariate_study.return_value = mock_univariate_instance

    mock_st.session_state = {
        "recipes_df": pd.DataFrame(
            {
                "submitted": pd.date_range(start="1999-01-01", periods=100, freq="YE"),
                "comment_count": range(100),
                "mean_rating": [4.5] * 100,
                "minutes": [30] * 100,
            }
        ),
        "first_load": True,
        "locked_graphs": {},
    }

    # Exécuter la fonction main
    with patch("src.pages.1_Analyse_des_donnees.st", mock_st):
        mock_st.title = MagicMock()
        mock_st.header = MagicMock()
        mock_st.error = MagicMock()

        main()

        # Assertions pour vérifier les appels attendus
        mock_load_css.assert_called_once_with("src/style.css")
        mock_compute_trend.assert_called_once_with(mock_st.session_state["recipes_df"])

        # Vérifier que les classes BivariateStudy et UnivariateStudy ont été appelées correctement
        assert mock_bivariate_study.call_count == 7
        assert mock_univariate_study.call_count == 6

        # # Vérifier que les graphiques sont ajoutés au locked_graphs
        # assert "Moyenne glissante du nombre de recettes" in mock_st.session_state["locked_graphs"]
        # assert "Nombre de recettes en fonction du temps" in mock_st.session_state["locked_graphs"]
        # assert "Nombre de commentaires par recette en fonction du temps" in mock_st.session_state["locked_graphs"]
        # assert "Nombre de recettes durant le pic d'activité du site" in mock_st.session_state["locked_graphs"]
        # assert "Distribution du nombre de commentaires par recette" in mock_st.session_state["locked_graphs"]
        # assert "Durée des recettes populaires" in mock_st.session_state["locked_graphs"]

        # Vérifier que la première charge est désactivée
        assert not mock_st.session_state["first_load"]

        # Vérifier que st.header et st.title ont été appelés
        mock_st.title.assert_called_once_with("Analyse des data")
        assert mock_st.header.call_count == 1

        # Vérifier les affichages de graphiques
        assert mock_bivariate_instance.display_graph.call_count == 1
        assert mock_univariate_instance.display_graph.call_count == 0


# Exception handling
@patch("src.pages.1_Analyse_des_donnees.compute_trend")
@patch("src.pages.1_Analyse_des_donnees.BivariateStudy")
@patch("src.pages.1_Analyse_des_donnees.UnivariateStudy")
@patch("src.pages.1_Analyse_des_donnees.load_css")
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
