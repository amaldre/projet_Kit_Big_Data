import pytest
from unittest.mock import patch, MagicMock
from src.pages.DataViz import main

@patch("src.pages.DataViz.st")  # Mock Streamlit
def test_main(mock_st):
    # Configuration des mocks
    mock_st.session_state = {
        "graph": [],  # Initialise la liste de graphes
        "recipes_df": MagicMock(),  # Mock du DataFrame des recettes
    }
    mock_st.columns.return_value = [MagicMock(), MagicMock()]  # Mock des colonnes
    mock_st.button.side_effect = [False, False]  # Mock des boutons : aucun bouton cliqué

    # Appel de la fonction principale
    main()

    # Vérifications
    mock_st.columns.assert_called_once_with(2)  # Vérifie si les colonnes ont été définies
    mock_st.button.assert_any_call("Ajout graphe univarié")  # Vérifie le bouton univarié
    mock_st.button.assert_any_call("Ajout graphe bivarié")  # Vérifie le bouton bivarié

@patch("src.pages.DataViz.st")
def test_main_add_univariate_graph(mock_st):
    # Mocking session_state et boutons
    mock_st.session_state = {
        "graph": [],
        "recipes_df": MagicMock(),
    }
    mock_st.columns.return_value = [MagicMock(), MagicMock()]
    mock_st.button.side_effect = [True, False]  # Mock du clic sur le bouton univarié

    # Appel de la fonction principale
    with patch("src.pages.DataViz.UnivariateStudy") as mock_univariate_study:
        mock_instance = MagicMock()
        mock_univariate_study.return_value = mock_instance
        main()

        # Vérifie qu'un graphe univarié a été ajouté
        assert len(mock_st.session_state["graph"]) == 1
        mock_univariate_study.assert_called_once()
        mock_st.rerun.assert_called_once()

@patch("src.pages.DataViz.st")
def test_main_add_bivariate_graph(mock_st):
    # Mocking session_state et boutons
    mock_st.session_state = {
        "graph": [],
        "recipes_df": MagicMock(),
    }
    mock_st.columns.return_value = [MagicMock(), MagicMock()]
    mock_st.button.side_effect = [False, True]  # Mock du clic sur le bouton bivarié

    # Appel de la fonction principale
    with patch("src.pages.DataViz.BivariateStudy") as mock_bivariate_study:
        mock_instance = MagicMock()
        mock_bivariate_study.return_value = mock_instance
        main()

        # Vérifie qu'un graphe bivarié a été ajouté
        assert len(mock_st.session_state["graph"]) == 1
        mock_bivariate_study.assert_called_once()
        mock_st.rerun.assert_called_once()

@patch("src.pages.DataViz.st")
def test_main_error_handling(mock_st):
    # Mocking session_state et boutons
    mock_st.session_state = {
        "graph": [],
        "recipes_df": MagicMock(),
    }
    mock_st.columns.return_value = [MagicMock(), MagicMock()]
    mock_st.button.side_effect = [True, False]  # Mock du clic sur le bouton univarié

    # Force une exception dans UnivariateStudy
    with patch("src.pages.DataViz.UnivariateStudy", side_effect=Exception("Test Error")):
        main()

        # Vérifie qu'une erreur a été loguée et affichée
        mock_st.error.assert_called_once_with(
            "Une erreur est survenue lors de l'affichage ou de la suppression d'un graphique."
        )