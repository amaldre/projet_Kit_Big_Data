# tests/test_pipeline_preprocess.py

import sys
import os
import pytest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.pipeline_preprocess import load_data


def test_load_data(tmp_path):
    # Créer un DataFrame de test
    test_df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})

    # Sauvegarder le DataFrame dans un fichier CSV temporaire
    test_csv_path = tmp_path / "test_data.csv"
    test_df.to_csv(test_csv_path, index=False)

    # Appeler la fonction
    result_df = load_data(test_csv_path)

    # Vérifier que le DataFrame chargé est identique au DataFrame initial
    pd.testing.assert_frame_equal(result_df, test_df)


from scripts.pipeline_preprocess import change_to_date_time_format


def test_change_to_date_time_format():
    # Créer un DataFrame de test
    data = pd.DataFrame({"date_column": ["2021-01-01", "2022-12-31"]})

    # Appeler la fonction
    result = change_to_date_time_format(data.copy(), "date_column")

    # Vérifier le type de la colonne
    assert result["date_column"].dtype == "O"  # 'O' pour 'object' en pandas

    # Vérifier les valeurs
    assert result["date_column"].iloc[0] == pd.to_datetime("2021-01-01").date()
    assert result["date_column"].iloc[1] == pd.to_datetime("2022-12-31").date()


from scripts.pipeline_preprocess import change_to_list


def test_change_to_list():
    data = pd.DataFrame({"list_column": ["[1, 2, 3]", "['a', 'b', 'c']"]})

    result = change_to_list(data.copy(), "list_column")

    # Vérifier le type de la colonne
    assert isinstance(result["list_column"].iloc[0], list)
    assert isinstance(result["list_column"].iloc[1], list)

    # Vérifier les valeurs
    assert result["list_column"].iloc[0] == [1, 2, 3]
    assert result["list_column"].iloc[1] == ["a", "b", "c"]


from scripts.pipeline_preprocess import delete_outliers_minutes


def test_delete_outliers_minutes():
    data = pd.DataFrame({"minutes": [5, 10, 15, 9999, 10000, 0]})

    result = delete_outliers_minutes(data.copy())

    # Les deux plus grandes valeurs et les valeurs égales à 0 doivent être supprimées
    expected_minutes = [5, 10, 15]
    assert list(result["minutes"]) == expected_minutes


from scripts.pipeline_preprocess import get_stopwords


def test_get_stopwords():
    stopwords = get_stopwords()
    assert isinstance(stopwords, set)
    # Vérifier que des mots spécifiques sont dans les stopwords
    assert "the" in stopwords
    assert "and" in stopwords
    assert "recipe" in stopwords  # Custom stopword


from unittest.mock import patch
from scripts.pipeline_preprocess import load_nltk_resources


def test_load_nltk_resources():
    # Patch `nltk.download` pour éviter les téléchargements réels
    with patch("scripts.pipeline_preprocess.nltk.download") as mock_download:
        # Exécuter la fonction
        load_nltk_resources()

        # Vérifier que `nltk.download` a été appelée pour chaque ressource
        mock_download.assert_any_call("punkt_tab")
        mock_download.assert_any_call("averaged_perceptron_tagger")
        mock_download.assert_any_call("wordnet")
        mock_download.assert_any_call("stopwords")

        # Vérifier que `nltk.download` a été appelée exactement 4 fois
        assert mock_download.call_count == 4


from scripts.pipeline_preprocess import change_to_str


def test_change_to_str():
    # Cas 1 : La colonne contient des listes
    data_with_lists = pd.DataFrame(
        {"list_column": [["a", "b", "c"], ["d", "e"], ["f"]]}
    )
    result = change_to_str(data_with_lists.copy(), "list_column")
    expected = pd.DataFrame({"list_column": ["a b c", "d e", "f"]})
    assert result.equals(
        expected
    ), "Échec de la conversion de la colonne de listes en chaîne de caractères"

    # Cas 2 : La colonne contient des entiers
    data_with_ints = pd.DataFrame({"int_column": [1, 2, 3]})
    result = change_to_str(data_with_ints.copy(), "int_column")
    expected = pd.DataFrame({"int_column": ["1", "2", "3"]})
    assert result.equals(
        expected
    ), "Échec de la conversion de la colonne d'entiers en chaîne de caractères"

    # Cas 3 : La colonne contient des flottants
    data_with_floats = pd.DataFrame({"float_column": [1.0, 2.5, 3.75]})
    result = change_to_str(data_with_floats.copy(), "float_column")
    expected = pd.DataFrame({"float_column": ["1.0", "2.5", "3.75"]})
    assert result.equals(
        expected
    ), "Échec de la conversion de la colonne de flottants en chaîne de caractères"

    # Cas 4 : La colonne contient déjà des chaînes de caractères
    data_with_strings = pd.DataFrame({"string_column": ["a", "b", "c"]})
    result = change_to_str(data_with_strings.copy(), "string_column")
    expected = pd.DataFrame({"string_column": ["a", "b", "c"]})
    assert result.equals(
        expected
    ), "Échec de la manipulation de la colonne de chaînes de caractères"


from scripts.pipeline_preprocess import change_category


def test_change_category():
    data = pd.DataFrame({"category_column": ["a", "b", "c"]})

    result = change_category(data.copy(), "category_column")

    # Vérifier le type de la colonne
    assert result["category_column"].dtype == "category"

    # Vérifier les valeurs
    assert result["category_column"].iloc[0] == "a"
    assert result["category_column"].iloc[1] == "b"
    assert result["category_column"].iloc[2] == "c"


from scripts.pipeline_preprocess import merge_dataframe


def test_merge_dataframe():
    # Créer deux DataFrames de test
    df1 = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df2 = pd.DataFrame({"col1": [1, 2], "col4": ["c", "d"]})

    # Appeler la fonction
    result = merge_dataframe(df1, df2, lefton="col1", righton="col1")

    # Vérifier le résultat
    expected = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"], "col4": ["c", "d"]})

    pd.testing.assert_frame_equal(result, expected)


from scripts.pipeline_preprocess import change_na_description_by_name


def test_change_na_description_by_name():

    data = pd.DataFrame(
        {
            "name": ["John", "Alice", "Bob"],
            "description": ["description1", "description2", None],
        }
    )

    result = change_na_description_by_name(data.copy())

    assert result["description"].iloc[2] == "Bob"


from scripts.pipeline_preprocess import delete_outliers_steps


def test_delete_outliers_steps():

    data = pd.DataFrame({"n_steps": [5, 10, 0]})

    result = delete_outliers_steps(data.copy())

    # Les deux plus grandes valeurs et les valeurs égales à 0 doivent être supprimées
    expected_steps = [5, 10]
    assert list(result["n_steps"]) == expected_steps


from scripts.pipeline_preprocess import groupby


def test_groupby():

    data = pd.DataFrame(
        {
            "recipe_id": [1, 1, 2, 2],
            "i": [0, 1, 2, 3],
            "name_tokens": ["token1", "token1", "token2", "token2"],
            "ingredient_tokens": ["ing1", "ing1", "ing2", "ing2"],
            "steps_tokens": ["step1", "step1", "step2", "step2"],
            "techniques": ["tech1", "tech1", "tech2", "tech2"],
            "calorie_level": ["low", "low", "high", "high"],
            "ingredient_ids": ["id1", "id1", "id2", "id2"],
            "name": ["name1", "name1", "name2", "name2"],
            "minutes": [10, 10, 20, 20],
            "contributor_id": [100, 100, 200, 200],
            "submitted": ["2020-01-01", "2020-01-01", "2020-01-02", "2020-01-02"],
            "tags": ["tag1", "tag1", "tag2", "tag2"],
            "nutrition": ["nut1", "nut1", "nut2", "nut2"],
            "steps": ["steps1", "steps1", "steps2", "steps2"],
            "n_steps": [1, 1, 2, 2],
            "description": ["desc1", "desc1", "desc2", "desc2"],
            "ingredients": ["ingr1", "ingr1", "ingr2", "ingr2"],
            "n_ingredients": [3, 3, 4, 4],
            "review": ["good", "bad", "excellent", "poor"],
            "date": ["2020-02-01", "2020-02-02", "2020-02-03", "2020-02-04"],
            "user_id": [1000, 1001, 1002, 1003],
            "rating": [5, 3, 4, 2],
        }
    )

    result = groupby(data)

    expected = pd.DataFrame(
        {
            "recipe_id": [1, 2],
            "i": [0, 2],
            "name_tokens": ["token1", "token2"],
            "ingredient_tokens": ["ing1", "ing2"],
            "steps_tokens": ["step1", "step2"],
            "techniques": ["tech1", "tech2"],
            "calorie_level": ["low", "high"],
            "ingredient_ids": ["id1", "id2"],
            "name": ["name1", "name2"],
            "minutes": [10, 20],
            "contributor_id": [100, 200],
            "submitted": ["2020-01-01", "2020-01-02"],
            "tags": ["tag1", "tag2"],
            "nutrition": ["nut1", "nut2"],
            "steps": ["steps1", "steps2"],
            "n_steps": [1, 2],
            "description": ["desc1", "desc2"],
            "ingredients": ["ingr1", "ingr2"],
            "n_ingredients": [3, 4],
            "review": [["good", "bad"], ["excellent", "poor"]],
            "date": [["2020-02-01", "2020-02-02"], ["2020-02-03", "2020-02-04"]],
            "user_id": [[1000, 1001], [1002, 1003]],
            "rating": [[5, 3], [4, 2]],
        }
    )

    expected = expected[result.columns]
    pd.testing.assert_frame_equal(result, expected)


from unittest.mock import patch
from scripts.pipeline_preprocess import clean_and_tokenize


@patch(
    "nltk.word_tokenize",
    return_value=[
        "hello",
        "this",
        "is",
        "a",
        "simple",
        "test",
        "with",
        "numbers",
        "and",
        "punctuation",
    ],
)
@patch(
    "nltk.pos_tag",
    return_value=[
        ("hello", "NN"),
        ("this", "DT"),
        ("is", "VBZ"),
        ("a", "DT"),
        ("simple", "JJ"),
        ("test", "NN"),
        ("with", "IN"),
        ("numbers", "NNS"),
        ("and", "CC"),
        ("punctuation", "NN"),
    ],
)
def test_clean_and_tokenize(mock_pos_tag, mock_word_tokenize):
    # Input text et stopwords pour le test
    text = "Hello! This is a simple test, with 123 numbers and punctuation."
    stopwords = {"is", "and", "with"}

    result = clean_and_tokenize(text, stopwords)

    # Vérification du résultat attendu
    expected_result = ["hello", "test", "numbers", "punctuation"]
    assert result == expected_result


from scripts.pipeline_preprocess import clean_colonne


@patch("scripts.pipeline_preprocess.clean_and_tokenize")
def test_clean_colonne(mock_clean_and_tokenize):
    mock_clean_and_tokenize.side_effect = [
        ["cleaned", "text1"],
        ["cleaned", "text2"]
    ]

    data = pd.DataFrame({
        "text_column": ["Text to clean 1", "Text to clean 2"]
    })
    stopwords = {"to", "clean"}

    result = clean_colonne(data.copy(), "text_column", stopwords)

    expected = pd.DataFrame({
        "text_column": ["Text to clean 1", "Text to clean 2"],
        "cleaned_text_column": [["cleaned", "text1"], ["cleaned", "text2"]]
    })

    pd.testing.assert_frame_equal(result, expected)
    mock_clean_and_tokenize.assert_any_call("Text to clean 1", stopwords)
    mock_clean_and_tokenize.assert_any_call("Text to clean 2", stopwords)
    assert mock_clean_and_tokenize.call_count == 2


from scripts.pipeline_preprocess import ingredient_to_ingredient_processed


def test_ingredient_to_ingredient_processed():
    ingredients = ["flour", "roman salad", "pink salt", "letuce"]

    processed_dict = {
        "flour": "flour",
        "roman salad": "salad",
        "pink salt": "salt",
        "letuce": "letuce",
    }
    replaced_dict = {
        "flour": "flour",
        "roman salad": "salad",
        "pink salt": "salt",
        "letuce": "salad",
    }

    result_processed, result_replaced = ingredient_to_ingredient_processed(
        ingredients, processed_dict, replaced_dict
    )

    expected_processed = ["flour", "salad", "salt", "letuce"]
    expected_replaced = ["flour", "salad", "salt", "salad"]

    assert result_processed == expected_processed
    assert result_replaced == expected_replaced


from scripts.pipeline_preprocess import save_data


def test_save_data(tmp_path):
    test_df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    test_csv_path = tmp_path / "test_data.csv"
    save_data(test_df, test_csv_path)

    result_df = pd.read_csv(test_csv_path)
    pd.testing.assert_frame_equal(result_df, test_df)


from scripts.pipeline_preprocess import save_data_json


def test_save_data_json(tmp_path):

    test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    test_json_path = tmp_path / "test_data.json"

    save_data_json(test_df, test_json_path)

    result_df = pd.read_json(test_json_path, lines=True)
    pd.testing.assert_frame_equal(result_df, test_df)


from scripts.pipeline_preprocess import explicit_nutriments


def test_explicit_nutriments_valid():
    data = pd.DataFrame({
        "nutrition": ["[100, 10, 5, 200, 15, 3, 50]", "[200, 20, 10, 400, 30, 6, 100]"]
    })
    result = explicit_nutriments(data.copy())
    
    expected = pd.DataFrame({
        "nutrition": ["[100, 10, 5, 200, 15, 3, 50]", "[200, 20, 10, 400, 30, 6, 100]"],
        "calories": ["100", "200"],
        "total fat (%)": ["10", "20"],
        "sugar (%)": ["5", "10"],
        "sodium (%)": ["200", "400"],
        "protein (%)": ["15", "30"],
        "saturated fat (%)": ["3", "6"],
        "carbohydrates (%)": ["50", "100"]
    })
    
    pd.testing.assert_frame_equal(result, expected)

def test_explicit_nutriments_missing_column():
    data = pd.DataFrame({
        "other_column": ["value1", "value2"]
    })
    
    with pytest.raises(ValueError, match="The 'nutrition' column is missing from the data."):
        explicit_nutriments(data)

def test_explicit_nutriments_invalid_format():
    data = pd.DataFrame({
        "nutrition": ["invalid_format"]
    })
    
    with pytest.raises(ValueError, match="Error processing 'nutrition' column:"):
        explicit_nutriments(data)


from scripts.pipeline_preprocess import change_techniques_to_words


def test_change_techniques_to_words():
    data = pd.DataFrame({
        "techniques": [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    })

    result = change_techniques_to_words(data.copy())

    expected = pd.DataFrame({
        "techniques": [
            ["bake"],
            ["barbecue"]
        ]
    })

    pd.testing.assert_frame_equal(result, expected)


from scripts.pipeline_preprocess import explicit_nutriments


def test_explicit_nutriments_valid():
    data = pd.DataFrame({
        "nutrition": [[100, 10, 5, 200, 15, 3, 50], [200, 20, 10, 400, 30, 6, 100]]
    })
    result = explicit_nutriments(data.copy())
    
    expected = pd.DataFrame({
        "nutrition": [[100, 10, 5, 200, 15, 3, 50], [200, 20, 10, 400, 30, 6, 100]],
        "calories": [100, 200],
        "total fat (%)": [10, 20],
        "sugar (%)": [5, 10],
        "sodium (%)": [200, 400],
        "protein (%)": [15, 30],
        "saturated fat (%)": [3, 6],
        "carbohydrates (%)": [50, 100]
    })
    
    pd.testing.assert_frame_equal(result, expected)

def test_explicit_nutriments_missing_column():
    data = pd.DataFrame({
        "other_column": ["value1", "value2"]
    })
    
    with pytest.raises(ValueError, match="The 'nutrition' column is missing from the data."):
        explicit_nutriments(data)


def test_explicit_nutriments_invalid_format():
    data = pd.DataFrame({
        "nutrition": ["invalid_format"]
    })
    
    with pytest.raises(ValueError, match="Error processing 'nutrition' column:"):
        explicit_nutriments(data)


from scripts.pipeline_preprocess import create_colums_count
from scripts.pipeline_preprocess import create_mean_rating


def test_create_colums_count():
    data = pd.DataFrame({
        "rating": [[5, 4, 3], [2, 1], [], [4, 4, 4, 4]]
    })

    result = create_colums_count(data.copy())

    expected = pd.DataFrame({
        "rating": [[5, 4, 3], [2, 1], [], [4, 4, 4, 4]],
        "comment_count": [3, 2, 0, 4]
    })

    pd.testing.assert_frame_equal(result, expected)


def test_create_mean_rating():
    data = pd.DataFrame({
        "rating": [[5, 4, 3], [2, 1], [], [4, 4, 4, 4]]
    })

    result = create_mean_rating(data.copy())

    expected = pd.DataFrame({
        "rating": [[5, 4, 3], [2, 1], [], [4, 4, 4, 4]],
        "mean_rating": [4.0, 1.5, None, 4.0]
    })

    pd.testing.assert_frame_equal(result, expected)


def test_create_mean_rating_exception():
    data = pd.DataFrame({
        "ratings": [[5, 4, 3], [2, 1], [], [4, 4, 4, 4, 0]]
    })

    with pytest.raises(ValueError, match="Le DataFrame doit contenir une colonne 'rating'."):
        create_mean_rating(data)

from scripts.pipeline_preprocess import preprocess
from unittest.mock import patch, MagicMock


@patch("scripts.pipeline_preprocess.rename_column")
@patch("scripts.pipeline_preprocess.create_mean_rating")
@patch("scripts.pipeline_preprocess.create_colums_count")
@patch("scripts.pipeline_preprocess.load_nltk_resources")
@patch("scripts.pipeline_preprocess.load_data")
@patch("scripts.pipeline_preprocess.change_to_date_time_format")
@patch("scripts.pipeline_preprocess.change_to_list")
@patch("scripts.pipeline_preprocess.merge_dataframe")
@patch("scripts.pipeline_preprocess.groupby")
@patch("scripts.pipeline_preprocess.change_na_description_by_name")
@patch("scripts.pipeline_preprocess.change_category")
@patch("scripts.pipeline_preprocess.delete_outliers_minutes")
@patch("scripts.pipeline_preprocess.delete_outliers_steps")
@patch("scripts.pipeline_preprocess.get_stopwords")
@patch("scripts.pipeline_preprocess.clean_colonne")
@patch("scripts.pipeline_preprocess.processed_ingredient")
@patch("scripts.pipeline_preprocess.change_techniques_to_words")
@patch("scripts.pipeline_preprocess.explicit_nutriments")
@patch("scripts.pipeline_preprocess.delete_unwanted_columns")
@patch("scripts.pipeline_preprocess.delete_outliers_calories")
@patch("scripts.pipeline_preprocess.save_data")
@patch("scripts.pipeline_preprocess.save_data_json")
def test_preprocess(
    mock_save_data_json,
    mock_save_data,
    mock_delete_outliers_calories,
    mock_delete_unwanted_columns,
    mock_explicit_nutriments,
    mock_change_techniques_to_words,
    mock_processed_ingredient,
    mock_clean_colonne,
    mock_get_stopwords,
    mock_delete_outliers_steps,
    mock_delete_outliers_minutes,
    mock_change_category,
    mock_change_na_description_by_name,
    mock_groupby,
    mock_merge_dataframe,
    mock_change_to_list,
    mock_change_to_date_time_format,
    mock_load_data,
    mock_load_nltk_resources,
    mock_create_colums_count,
    mock_create_mean_rating,
    mock_rename_column,
):
    mock_load_data.side_effect = [
        pd.DataFrame({"id": [1, 2], "submitted": ["2021-01-01", "2021-01-02"], "rating": [[1, 1], [1, 1]]}),
        pd.DataFrame({"recipe_id": [1, 2], "date": ["2021-01-01", "2021-01-02"], "rating": [[1, 1], [1, 1]]}),
        pd.DataFrame({"id": [1, 2], "techniques": ["[1, 0]", "[0, 1]"], "rating": [[1, 1], [1, 1]]}),
    ]
    mock_get_stopwords.return_value = set(["stopword1", "stopword2"])

    preprocess()

    mock_load_nltk_resources.assert_called_once()
    assert mock_load_data.call_count == 3
    assert mock_change_to_date_time_format.call_count == 2
    assert mock_change_to_list.call_count == 5
    mock_merge_dataframe.assert_called()
    mock_groupby.assert_called_once()
    mock_change_na_description_by_name.assert_called_once()
    assert mock_change_category.call_count == 2
    mock_delete_outliers_minutes.assert_called_once()
    mock_delete_outliers_steps.assert_called_once()
    mock_get_stopwords.assert_called_once()
    assert mock_clean_colonne.call_count == 2
    mock_processed_ingredient.assert_called_once()
    mock_change_techniques_to_words.assert_called_once()
    mock_explicit_nutriments.assert_called_once()
    mock_delete_unwanted_columns.assert_called_once()
    mock_delete_outliers_calories.assert_called_once()
    mock_save_data.assert_called_once()
    mock_save_data_json.assert_called_once()
    mock_create_colums_count.assert_called_once()
    mock_create_mean_rating.assert_called_once()
    mock_rename_column.assert_called_once()
