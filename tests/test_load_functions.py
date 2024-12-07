import pytest
import pandas as pd
import os
import ast
from utils.load_functions import (
    load_csv,
    load_css,
    load_df,
    load_data,
    initialize_recipes_df,
    compute_trend,
)


def test_load_csv_valid_file(tmp_path):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(file_path, index=False)
    loaded_df = load_csv(str(file_path))
    assert loaded_df.equals(df)


def test_load_csv_file_not_found(tmp_path):
    file_path = tmp_path / "non_existent.csv"
    with pytest.raises(FileNotFoundError):
        load_csv(str(file_path))


def test_load_css_valid_file(tmp_path):
    file_path = tmp_path / "test.css"
    css_content = "body { background-color: blue; }"
    file_path.write_text(css_content, encoding="utf-8")
    load_css(str(file_path))


def test_load_css_file_not_found(tmp_path, caplog):
    file_path = tmp_path / "non_existent.css"
    load_css(str(file_path))
    assert "Le fichier CSS" in caplog.text
    assert "est introuvable" in caplog.text


def test_load_css_unexpected_error(tmp_path, monkeypatch, caplog):
    file_path = tmp_path / "test.css"
    css_content = "body { background-color: blue; }"
    file_path.write_text(css_content, encoding="utf-8")

    def mock_open(*args, **kwargs):
        raise Exception("Unexpected error")

    monkeypatch.setattr("builtins.open", mock_open)
    load_css(str(file_path))
    assert (
        "Une erreur inattendue s'est produite lors du chargement du CSS" in caplog.text
    )


def test_load_df_valid_file(tmp_path):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame(
        {
            "Ingrédients": ["['salt', 'pepper']", "['sugar']"],
            "Techniques utilisées": ["['bake']", "['fry']"],
            "Date de publication de la recette": ["2023-01-01", "2023-01-02"],
        }
    )
    df.to_csv(file_path, index=False)
    loaded_df = load_df(str(file_path))
    assert loaded_df["Ingrédients"].iloc[0] == ["salt", "pepper"]
    assert loaded_df["Nombre d'ingrédients"].iloc[0] == 2
    assert loaded_df["Techniques utilisées"].iloc[0] == ["bake"]
    assert loaded_df["Nombre de techniques utilisées"]    .iloc[0] == 1
    assert pd.to_datetime(loaded_df["Date de publication de la recette"].iloc[0]) == pd.to_datetime(
        "2023-01-01"
    )


def test_load_df_file_not_found(tmp_path):
    file_path = tmp_path / "non_existent.csv"
    with pytest.raises(FileNotFoundError):
        load_df(str(file_path))


def test_load_data_valid_file(tmp_path):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(file_path, index=False)
    loaded_df = load_data(str(tmp_path), "test.csv")
    assert loaded_df.equals(df)


def test_load_data_file_not_found(tmp_path, caplog):
    loaded_df = load_data(str(tmp_path), "non_existent.csv")
    assert loaded_df.empty
    assert "Fichier introuvable" in caplog.text


def test_load_data_unexpected_error(tmp_path, monkeypatch, caplog):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(file_path, index=False)

    def mock_read_csv(*args, **kwargs):
        raise Exception("Unexpected error")

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    loaded_df = load_data(str(tmp_path), "test.csv")
    assert loaded_df.empty
    assert "Erreur lors du chargement du fichier" in caplog.text


def test_initialize_recipes_df_valid_file(tmp_path):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame(
        {
            "Ingrédients": ["['salt', 'pepper']", "['sugar']"],
            "Techniques utilisées": ["['bake']", "['fry']"],
            "Date de publication de la recette": ["2023-01-01", "2023-01-02"],
        }
    )
    df.to_csv(file_path, index=False)
    loaded_df = initialize_recipes_df(str(file_path))
    assert loaded_df["Ingrédients"].iloc[0] == ["salt", "pepper"]
    assert loaded_df["Nombre d'ingrédients"].iloc[0] == 2
    assert loaded_df["Techniques utilisées"].iloc[0] == ["bake"]
    assert loaded_df["Nombre de techniques utilisées"].iloc[0] == 1
    assert pd.to_datetime(loaded_df["Date de publication de la recette"].iloc[0]) == pd.to_datetime(
        "2023-01-01"
    )


def test_initialize_recipes_df_file_not_found(tmp_path, caplog):
    file_path = tmp_path / "non_existent.csv"
    loaded_df = initialize_recipes_df(str(file_path))
    assert loaded_df.empty
    assert "Le fichier CSV" in caplog.text
    assert "est introuvable" in caplog.text


def test_initialize_recipes_df_parser_error(tmp_path, caplog):
    file_path = tmp_path / "malformed.csv"
    file_path.write_text('col1,col2\nval1,"val2\nval3,val4', encoding="utf-8")
    loaded_df = initialize_recipes_df(str(file_path))
    assert loaded_df.empty
    assert (
        "Erreur lors du traitement du fichier CSV. Veuillez vérifier son format." in caplog.text
    )


def test_initialize_recipes_df_unexpected_error(tmp_path, monkeypatch, caplog):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame(
        {
            "ingredients_replaced": ["['salt', 'pepper']", "['sugar']"],
            "techniques": ["['bake']", "['fry']"],
            "submitted": ["2023-01-01", "2023-01-02"],
        }
    )
    df.to_csv(file_path, index=False)

    def mock_load_df(*args, **kwargs):
        raise Exception("Unexpected error")

    monkeypatch.setattr("utils.load_functions.load_df", mock_load_df)
    loaded_df = initialize_recipes_df(str(file_path))
    assert loaded_df.empty
    assert (
        "Une erreur inattendue s'est produite lors du chargement du CSV" in caplog.text
    )


def test_compute_trend_valid_data():
    df = pd.DataFrame(
        {
            "Date de publication de la recette": pd.date_range(start="2021-01-01", periods=24, freq="ME"),
            "count": [10 * i for i in range(1, 25)],
        }
    )
    trend_df = compute_trend(df)
    assert "Date" in trend_df.columns
    assert "Moyenne glissante" in trend_df.columns
    assert len(trend_df.dropna()) > 0


def test_compute_trend_empty_data():
    df = pd.DataFrame(columns=["Date de publication de la recette", "count"])
    trend_df = compute_trend(df)
    assert trend_df.empty
