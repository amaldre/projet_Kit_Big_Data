# tests/test_classes.py

import sys
import os
import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
from utils.classes import bivariateStudy
from utils.univariateStudy import univariateStudy


def test_study_init():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame({"col1": [1, 2, 3]})
    axis_x_list = ["col1"]
    axis_y_list = ["col1"]
    filters = ["col1"]
    key = "test_key" 

    study = bivariateStudy(key, df, "plot_type", axis_x_list, axis_y_list, filters)

    assert study.dataframe.equals(df)
    assert study.axis_x_list == axis_x_list
    assert study.axis_y_list == axis_y_list
    assert study.filters == filters
    assert study.key == key
    assert study.delete == False


def test_study_get_data_points():
    # Créer un DataFrame d'exemple
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "axis_x": [1, 2, 3, 4, 5],
            "axis_y": [5, 4, 3, 2, 1],
            "filter_col": [10, 20, 30, 40, 50],
        }
    )
    axis_x_list = ["axis_x"]
    axis_y_list = ["axis_y"]
    filters = ["filter_col"]
    key = "test_key"

    study = bivariateStudy(key, df, "plot_type", axis_x_list, axis_y_list, filters)

    axis_x = "axis_x"
    axis_y = "axis_y"
    range_axis_x = (2, 4)
    range_axis_y = (2, 4)
    chosen_filters = ["filter_col"]
    range_filters = [(15, 35)]

    x_values, y_values, ids = study.get_data_points(
        df, axis_x, axis_y, range_axis_x, range_axis_y, chosen_filters, range_filters
    )

    # DataFrame attendu après filtrage
    expected_df = df[
        (df[axis_x] >= range_axis_x[0])
        & (df[axis_x] <= range_axis_x[1])
        & (df[axis_y] >= range_axis_y[0])
        & (df[axis_y] <= range_axis_y[1])
        & (df["filter_col"] >= range_filters[0][0])
        & (df["filter_col"] <= range_filters[0][1])
    ]

    assert list(x_values) == list(expected_df[axis_x])
    assert list(y_values) == list(expected_df[axis_y])
    assert list(ids) == list(expected_df["id"])

# AdvancedStudy

@pytest.fixture
def sample_dataframe():
    # Création d'un DataFrame de test
    data = {
        "axis_x": range(1, 101),
        "filter1": range(50, 150),
        "filter2": range(100, 200),
        "recipe_id": [f"recipe_{i}" for i in range(1, 101)],
        "comment_count": range(0, 100),
        "ingredients_replaced": [["ing1", "ing2", "ing3"]] * 100,
        "techniques": [["tech1", "tech2"]] * 100,
        "datetime_column": pd.date_range(
            start="2023-01-01", periods=100, freq="D"
        ),
    }
    return pd.DataFrame(data)

@pytest.fixture
def univariate_study_instance(sample_dataframe):
    # Création d'une instance de univariateStudy pour les tests
    return univariateStudy(
        key="test_key",
        dataframe=sample_dataframe,
        plot_type="normal",
        axis_x_list=["axis_x", "filter1", "datetime_column", "ingredients_replaced"],
        filters=["filter1", "filter2"],
        default_values={"axis_x": [10, 50]},
    )

def test_initialization(univariate_study_instance):
    # Test de l'initialisation
    assert univariate_study_instance.key == "test_key"
    assert univariate_study_instance.plot_type == "normal"
    assert univariate_study_instance.axis_x_list == ["axis_x", "filter1", "datetime_column", "ingredients_replaced"]

def test_set_axis(univariate_study_instance):
    # Test de la sélection d'un axe X
    univariate_study_instance.axis_x = "filter1"
    assert univariate_study_instance.axis_x == "filter1"

def test_set_range_axis(univariate_study_instance, sample_dataframe):
    # Test de la définition d'un slider pour un axe donné
    range_axis = univariate_study_instance._univariateStudy__create_slider_from_df(
        sample_dataframe, "axis_x"
    )
    assert isinstance(range_axis, list) or isinstance(range_axis, tuple)

def test_get_data_points(univariate_study_instance):
    # Test de récupération des points de données
    x_values, recipe_ids = univariate_study_instance.get_data_points(
        univariate_study_instance.dataframe,
        "axis_x",
        [10, 50],
        ["filter1"],
        [[60, 80]],
    )
    assert len(x_values) > 0
    assert all(x >= 10 and x <= 50 for x in x_values)

def test_get_data_points_ingredients(univariate_study_instance):
    # Test de récupération des points de données pour les ingrédients
    elements, counts, recipe_ids = univariate_study_instance.get_data_points_ingredients(
        univariate_study_instance.dataframe,
        "ingredients_replaced",
        5,
        [],
        [],
    )
    assert len(elements) == 5
    assert isinstance(elements[0], str)

def test_graph_methods(univariate_study_instance):
    # Test des méthodes de tracé
    x_values, recipe_ids = univariate_study_instance.get_data_points(
        univariate_study_instance.dataframe,
        "axis_x",
        [10, 50],
        [],
        [],
    )
    # Normal plot
    univariate_study_instance.graph_normal(x_values)

    # Boxplot
    univariate_study_instance.graph_boxplot(x_values)

    # Density plot
    univariate_study_instance.graph_density(x_values)

    # Histogram
    univariate_study_instance.graph_histogram(x_values)

def test_filter_functionality(univariate_study_instance):
    # Test des fonctionnalités de filtrage
    chosen_filters, range_filters = univariate_study_instance._univariateStudy__filters(
        "axis_x"
    )
    assert isinstance(chosen_filters, list)
    assert isinstance(range_filters, list)

def test_save_graph(univariate_study_instance):
    # Test de la sauvegarde des attributs du graphique
    univariate_study_instance.axis_x = "filter1"
    univariate_study_instance.range_axis_x = [10, 50]
    univariate_study_instance.save_graph()
    assert univariate_study_instance.default_values["filter1"] == [10, 50]

def test_date_range_filter(univariate_study_instance):
    # Test de la gestion des colonnes de type datetime
    start_date, end_date = univariate_study_instance._univariateStudy__set_date("datetime_column")
    assert isinstance(start_date, pd.Timestamp)
    assert isinstance(end_date, pd.Timestamp)
    assert start_date <= end_date

def test_ingredient_bar_chart(univariate_study_instance):
    # Test du tracé des barres pour les ingrédients
    elements, counts, recipe_ids = univariate_study_instance.get_data_points_ingredients(
        univariate_study_instance.dataframe,
        "ingredients_replaced",
        3,
        [],
        [],
    )
    assert len(elements) == 3
    univariate_study_instance.graph_bar_elts(elements, counts)

def test_technique_bar_chart(univariate_study_instance):
    # Test du tracé des barres pour les techniques
    elements, counts, recipe_ids = univariate_study_instance.get_data_points_ingredients(
        univariate_study_instance.dataframe,
        "techniques",
        2,
        [],
        [],
    )
    assert len(elements) == 2
    univariate_study_instance.graph_bar_elts(elements, counts)

data = pd.DataFrame({
    "axis1": [1, 2, 3, 4, 5],
    "axis2": [10, 20, 30, 40, 50],
    "date_column": pd.date_range(start="2023-01-01", periods=5),
    "ingredients_replaced": [["sugar"], ["salt", "pepper"], ["sugar"], ["honey"], ["sugar", "honey"]],
    "recipe_id": [101, 102, 103, 104, 105],
    "comment_count": [5, 15, 10, 0, 8],
})

@patch("streamlit.selectbox", return_value="axis1")
@patch("streamlit.slider", return_value=(1, 5))
@patch("streamlit.multiselect", return_value=["axis2"])
@patch("streamlit.form_submit_button", side_effect=[True, False])  # Simule des clics sur les boutons
@patch("streamlit.empty")
def test_display_graph(mock_empty, mock_button, mock_multiselect, mock_slider, mock_selectbox):
    # Teste la méthode `display_graph`
    obj = univariateStudy(
        key="test_key",
        dataframe=data,
        plot_type="normal",
        axis_x_list=["axis1", "axis2"],
        filters=["axis1", "axis2"],
        default_values={"axis1": [1, 5], "chosen_filters": ["axis2"], "axis2": [10, 50]},
    )

    # Mock l'objet container pour simuler l'interface graphique Streamlit
    mock_container = MagicMock()
    mock_empty.return_value = mock_container

    # Exécute la méthode display_graph
    obj.display_graph()

    # Vérifie si les widgets Streamlit ont été appelés avec les bons paramètres
    mock_selectbox.assert_called_once_with(
        label="axis_x", options=["axis1", "axis2"], key="axis_xtest_key1"
    )
    mock_slider.assert_called_once_with(
        label="Range for axis1", min_value=1, max_value=5, value=(1, 5), step=1, key="axis1test_key1"
    )
    mock_multiselect.assert_called_once_with(
        label="filters",
        default=["axis2"],
        options=["axis1", "axis2"],
        key="filterstest_key1",
    )
    mock_button.assert_any_call(label="Draw graph")
    mock_button.assert_any_call(label="Delete graph")

    # Vérifie si l'objet graphique a été dessiné
    assert obj.axis_x == "axis1"
    assert obj.range_axis_x == (1, 5)

@patch("streamlit.slider", return_value=10)
def test_set_number_ingredients(mock_slider):
    # Teste la méthode privée __set_number_ingredients
    obj = univariateStudy(
        key="test_key",
        dataframe=data,
        plot_type="bar_ingredients",
        axis_x_list=["ingredients_replaced"],
        filters=None,
        default_values={"ingredients_replaced": 10},
    )
    result = obj._univariateStudy__set_number_ingredients("ingredients_replaced")
    assert result == 10
    mock_slider.assert_called_once_with(
        label="Range for ingredients_replaced",
        min_value=1,
        max_value=15,
        value=10,
        step=1,
        key="ingredients_replacedtest_key1",
    )

@patch("streamlit.date_input")
def test_set_date(mock_date_input):
    # Mock les valeurs de date
    mock_date_input.side_effect = [datetime(2023, 1, 1), datetime(2023, 1, 5)]

    obj = univariateStudy(
        key="test_key",
        dataframe=data,
        plot_type="normal",
        axis_x_list=["date_column"],
        filters=None,
    )
    start_date, end_date = obj._univariateStudy__set_date("date_column")

    # Vérifie les résultats
    assert start_date == pd.Timestamp("2023-01-01")
    assert end_date == pd.Timestamp("2023-01-05")

    # Vérifie que les appels à date_input ont été faits
    mock_date_input.assert_any_call(
        "Start date",
        value=data["date_column"].min(),
        min_value=data["date_column"].min(),
        max_value=data["date_column"].max(),
        key="start datetest_key1",
    )
    mock_date_input.assert_any_call(
        "End date",
        value=data["date_column"].max(),
        min_value=pd.Timestamp("2023-01-01"),
        max_value=data["date_column"].max(),
        key="end datetest_key1",
    )






# def test_advancedstudy_init():
#     # Créer un Dataframe d'exemple
#     df = pd.DataFrame({"col1": [1, 2, 3]})
#     axis_x_list = ["col1"]
#     filters = ["col1"]
#     key = "test_key"

#     advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

#     assert advanced_study.dataframe.equals(df)
#     assert advanced_study.axis_x_list == axis_x_list
#     assert advanced_study.filters == filters
#     assert advanced_study.key == key
#     assert advanced_study.delete == False


# def test_advancedstudy_get_data_points():
#     # Créer un DataFrame d'exemple
#     df = pd.DataFrame(
#         {
#             "id": [1, 2, 3, 4, 5],
#             "axis_x": [1, 2, 3, 4, 5],
#             "filter_col": [10, 20, 30, 40, 50],
#         }
#     )
#     axis_x_list = ["axis_x"]
#     filters = ["filter_col"]
#     key = "test_key"

#     advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

#     axis_x = "axis_x"
#     range_axis_x = (2, 4)
#     chosen_filters = ["filter_col"]
#     range_filters = [(15, 35)]

#     x_values, ids = advanced_study.get_data_points(
#         df, axis_x, range_axis_x, chosen_filters, range_filters
#     )

#     # DataFrame attendu après filtrage
#     expected_df = df[
#         (df[axis_x] >= range_axis_x[0])
#         & (df[axis_x] <= range_axis_x[1])
#         & (df["filter_col"] >= range_filters[0][0])
#         & (df["filter_col"] <= range_filters[0][1])
#     ]

#     assert list(x_values) == list(expected_df[axis_x])
#     assert list(ids) == list(expected_df["id"])

# def test_get_data_points_ingredients():
#     # Créer un Dataframe d'exemple
#     df = pd.DataFrame({
#         "recipe_id": ["a", "b", "c"],
#         "ingredients_replaced": ["ing1", "ing2", "ing3"]
#     })
#     axis_x_list = ["ingredients_replaced"]
#     filters = []
#     key = "test_key"

#     advanced_study = AdvancedStudy(df, axis_x_list, filters, key)

#     result = advanced_study.get_data_points_ingredients(df)

#     assert list(result) == ["a", "b", "c"]