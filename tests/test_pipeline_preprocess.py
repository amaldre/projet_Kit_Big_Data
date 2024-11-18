# tests/test_pipeline_preprocess.py

import sys
import os
import pytest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.pipeline_preprocess import load_data

def test_load_data(tmp_path):
    # Créer un DataFrame de test
    test_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
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
    data = pd.DataFrame({
        'date_column': ['2021-01-01', '2022-12-31']
    })
    
    # Appeler la fonction
    result = change_to_date_time_format(data.copy(), 'date_column')
    
    # Vérifier le type de la colonne
    assert result['date_column'].dtype == 'O'  # 'O' pour 'object' en pandas
    
    # Vérifier les valeurs
    assert result['date_column'].iloc[0] == pd.to_datetime('2021-01-01').date()
    assert result['date_column'].iloc[1] == pd.to_datetime('2022-12-31').date()


from scripts.pipeline_preprocess import change_to_list

def test_change_to_list():
    data = pd.DataFrame({
        'list_column': ['[1, 2, 3]', "['a', 'b', 'c']"]
    })
    
    result = change_to_list(data.copy(), 'list_column')
    
    # Vérifier le type de la colonne
    assert isinstance(result['list_column'].iloc[0], list)
    assert isinstance(result['list_column'].iloc[1], list)
    
    # Vérifier les valeurs
    assert result['list_column'].iloc[0] == [1, 2, 3]
    assert result['list_column'].iloc[1] == ['a', 'b', 'c']

from scripts.pipeline_preprocess import delete_outliers_minutes

def test_delete_outliers_minutes():
    data = pd.DataFrame({
        'minutes': [5, 10, 15, 9999, 10000, 0]
    })
    
    result = delete_outliers_minutes(data.copy())
    
    # Les deux plus grandes valeurs et les valeurs égales à 0 doivent être supprimées
    expected_minutes = [5, 10, 15]
    assert list(result['minutes']) == expected_minutes


from scripts.pipeline_preprocess import get_stopwords

def test_get_stopwords():
    stopwords = get_stopwords()
    assert isinstance(stopwords, set)
    # Vérifier que des mots spécifiques sont dans les stopwords
    assert 'the' in stopwords
    assert 'and' in stopwords
    assert 'recipe' in stopwords  # Custom stopword

from unittest.mock import patch
from scripts.pipeline_preprocess import load_nltk_resources  

def test_load_nltk_resources():
    # Patch `nltk.download` pour éviter les téléchargements réels
    with patch('scripts.pipeline_preprocess.nltk.download') as mock_download:
        # Exécuter la fonction
        load_nltk_resources()

        # Vérifier que `nltk.download` a été appelée pour chaque ressource
        mock_download.assert_any_call('punkt_tab')
        mock_download.assert_any_call('averaged_perceptron_tagger')
        mock_download.assert_any_call('wordnet')
        mock_download.assert_any_call('stopwords')

        # Vérifier que `nltk.download` a été appelée exactement 4 fois
        assert mock_download.call_count == 4
        
from scripts.pipeline_preprocess import change_to_str


def test_change_to_str():
    # Cas 1 : La colonne contient des listes
    data_with_lists = pd.DataFrame({
        'list_column': [['a', 'b', 'c'], ['d', 'e'], ['f']]
    })
    result = change_to_str(data_with_lists.copy(), 'list_column')
    expected = pd.DataFrame({
        'list_column': ['a b c', 'd e', 'f']
    })
    assert result.equals(expected), "Échec de la conversion de la colonne de listes en chaîne de caractères"

    # Cas 2 : La colonne contient des entiers
    data_with_ints = pd.DataFrame({
        'int_column': [1, 2, 3]
    })
    result = change_to_str(data_with_ints.copy(), 'int_column')
    expected = pd.DataFrame({
        'int_column': ['1', '2', '3']
    })
    assert result.equals(expected), "Échec de la conversion de la colonne d'entiers en chaîne de caractères"

    # Cas 3 : La colonne contient des flottants
    data_with_floats = pd.DataFrame({
        'float_column': [1.0, 2.5, 3.75]
    })
    result = change_to_str(data_with_floats.copy(), 'float_column')
    expected = pd.DataFrame({
        'float_column': ['1.0', '2.5', '3.75']
    })
    assert result.equals(expected), "Échec de la conversion de la colonne de flottants en chaîne de caractères"

    # Cas 4 : La colonne contient déjà des chaînes de caractères
    data_with_strings = pd.DataFrame({
        'string_column': ['a', 'b', 'c']
    })
    result = change_to_str(data_with_strings.copy(), 'string_column')
    expected = pd.DataFrame({
        'string_column': ['a', 'b', 'c']
    })
    assert result.equals(expected), "Échec de la manipulation de la colonne de chaînes de caractères"

    

from scripts.pipeline_preprocess import change_category

def test_change_category():
    data = pd.DataFrame({
        'category_column': ['a', 'b', 'c']
    })
    
    result = change_category(data.copy(), 'category_column')
    
    # Vérifier le type de la colonne
    assert result['category_column'].dtype == 'category'
    
    # Vérifier les valeurs
    assert result['category_column'].iloc[0] == 'a'
    assert result['category_column'].iloc[1] == 'b'
    assert result['category_column'].iloc[2] == 'c'

from scripts.pipeline_preprocess import merge_dataframe
  
def test_merge_dataframe():
    # Créer deux DataFrames de test
    df1 = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    df2 = pd.DataFrame({'col1': [1, 2], 'col4': ['c', 'd']})
    
    # Appeler la fonction
    result = merge_dataframe(df1, df2, lefton='col1', righton='col1')

    # Vérifier le résultat
    expected = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b'],
        'col4': ['c', 'd']
    })
    
    pd.testing.assert_frame_equal(result, expected)

from scripts.pipeline_preprocess import change_na_description_by_name

def test_change_na_description_by_name():
    
    data = pd.DataFrame({
        'name': ['John', 'Alice', 'Bob'],
        'description': ['description1', 'description2', None]
    })
    
    result = change_na_description_by_name(data.copy())

    assert result['description'].iloc[2] == 'Bob'
    

from scripts.pipeline_preprocess import delete_outliers_steps

def test_delete_outliers_steps():
    
    data = pd.DataFrame({
        'n_steps': [5, 10, 0]
    })
    
    result = delete_outliers_steps(data.copy())
    
    # Les deux plus grandes valeurs et les valeurs égales à 0 doivent être supprimées
    expected_steps = [5, 10]
    assert list(result['n_steps']) == expected_steps
    

from scripts.pipeline_preprocess import groupby

def test_groupby():

    data = pd.DataFrame({
        'recipe_id': [1, 1, 2, 2],
        'i': [0, 1, 2, 3],
        'name_tokens': ['token1', 'token1', 'token2', 'token2'],
        'ingredient_tokens': ['ing1', 'ing1', 'ing2', 'ing2'],
        'steps_tokens': ['step1', 'step1', 'step2', 'step2'],
        'techniques': ['tech1', 'tech1', 'tech2', 'tech2'],
        'calorie_level': ['low', 'low', 'high', 'high'],
        'ingredient_ids': ['id1', 'id1', 'id2', 'id2'],
        'name': ['name1', 'name1', 'name2', 'name2'],
        'minutes': [10, 10, 20, 20],
        'contributor_id': [100, 100, 200, 200],
        'submitted': ['2020-01-01', '2020-01-01', '2020-01-02', '2020-01-02'],
        'tags': ['tag1', 'tag1', 'tag2', 'tag2'],
        'nutrition': ['nut1', 'nut1', 'nut2', 'nut2'],
        'steps': ['steps1', 'steps1', 'steps2', 'steps2'],
        'n_steps': [1, 1, 2, 2],
        'description': ['desc1', 'desc1', 'desc2', 'desc2'],
        'ingredients': ['ingr1', 'ingr1', 'ingr2', 'ingr2'],
        'n_ingredients': [3, 3, 4, 4],
        'review': ['good', 'bad', 'excellent', 'poor'],
        'date': ['2020-02-01', '2020-02-02', '2020-02-03', '2020-02-04'],
        'user_id': [1000, 1001, 1002, 1003],
        'rating': [5, 3, 4, 2]
    })


    result = groupby(data)
    
    expected = pd.DataFrame({
        'recipe_id': [1, 2],
        'i': [0, 2],
        'name_tokens': ['token1', 'token2'],
        'ingredient_tokens': ['ing1', 'ing2'],
        'steps_tokens': ['step1', 'step2'],
        'techniques': ['tech1', 'tech2'],
        'calorie_level': ['low', 'high'],
        'ingredient_ids': ['id1', 'id2'],
        'name': ['name1', 'name2'],
        'minutes': [10, 20],
        'contributor_id': [100, 200],
        'submitted': ['2020-01-01', '2020-01-02'],
        'tags': ['tag1', 'tag2'],
        'nutrition': ['nut1', 'nut2'],
        'steps': ['steps1', 'steps2'],
        'n_steps': [1, 2],
        'description': ['desc1', 'desc2'],
        'ingredients': ['ingr1', 'ingr2'],
        'n_ingredients': [3, 4],
        'review': [['good', 'bad'], ['excellent', 'poor']],
        'date': [['2020-02-01', '2020-02-02'], ['2020-02-03', '2020-02-04']],
        'user_id': [[1000, 1001], [1002, 1003]],
        'rating': [[5, 3], [4, 2]]
    })

    expected = expected[result.columns]
    pd.testing.assert_frame_equal(result, expected)


from scripts.pipeline_preprocess import clean_and_tokenize

def test_clean_and_tokenize(self):

    string = 'This is a test.'
    stopwords = {'is', 'a', 'another'}
    
    expected_result = ['this', 'test']
    

    result = clean_and_tokenize(string, stopwords)

    self.assertEqual(result, expected_result)