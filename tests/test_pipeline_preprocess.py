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
    data = pd.DataFrame({
        'int_column': [1, 2, 3],
        'float_column': [1.0, 2.0, 3.0]
    })
    
    result = change_to_str(data.copy(), ['int_column', 'float_column'])
    
    # Vérifier le type de la colonne
    assert result.dtypes['int_column'] == object  # Utilisez result.dtypes
    assert result.dtypes['float_column'] == object
    
    # Vérifier les valeurs
    assert result['int_column'].iloc[0] == '1'
    assert result['float_column'].iloc[0] == '1.0'

    

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
    
def merge_dataframes():
    # Créer deux DataFrames de test
    df1 = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    df2 = pd.DataFrame({'col1': [1, 2], 'col2': ['c', 'd']})
    
    # Appeler la fonction
    result = merge_dataframes(df1, df2, lefton='col1', righton='col1')

    # Vérifier le résultat
    expected = pd.DataFrame({
        'col1': [1, 2],
        'col2_x': ['a', 'b'],
        'col2_y': ['c', 'd']
    })
    
    pd.testing.assert_frame_equal(result, expected)

