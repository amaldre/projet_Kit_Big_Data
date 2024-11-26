import sys
import os
import pytest
from unittest.mock import patch, MagicMock


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dbapi import DBapi

def test_dbapi_init():
    with patch('src.dbapi.os.getenv') as mock_getenv, \
         patch('src.dbapi.MongoClient') as mock_mongo_client:

        mock_getenv.return_value = 'mongodb://localhost:27017'
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance


        db_api = DBapi()

        # Assertions
        mock_getenv.assert_called_once_with('URI_DB')
        mock_mongo_client.assert_called_once_with('mongodb://localhost:27017')
        assert db_api.client == mock_client_instance
        assert db_api.db == mock_client_instance["MangaTaMainDF"]
        assert db_api.collection == db_api.db["Food.com"]

@patch('os.getenv')
def test_dbapi_find_by(mock_getenv):
    mock_getenv.return_value = "mongodb://mock_uri"
    with patch('src.dbapi.MongoClient') as mock_mongo_client:
        mock_collection = MagicMock()
        mock_db = {'Food.com': mock_collection}
        mock_client_instance = {'MangaTaMainDF': mock_db}
        mock_mongo_client.return_value = mock_client_instance

        db_api = DBapi()

        db_api.client = mock_client_instance
        db_api.db = mock_client_instance['MangaTaMainDF']
        db_api.collection = mock_collection

        # Configurer find().limit()
        mock_find = MagicMock()
        mock_collection.find.return_value = mock_find
        mock_find.limit.return_value = ['doc1', 'doc2']

        # Appeler la méthode
        result = db_api.find_by('test_col', 'test_value', nb=2)

        # Assertions
        mock_collection.find.assert_called_once_with({'test_col': 'test_value'})
        mock_find.limit.assert_called_once_with(2)
        assert result == ['doc1', 'doc2']

def test_dbapi_find_range_submitted():
    with patch('src.dbapi.MongoClient') as mock_mongo_client:
        # Mock de la collection
        mock_collection = MagicMock()
        mock_db = {'Food.com': mock_collection}
        mock_client_instance = {'MangaTaMainDF': mock_db}
        mock_mongo_client.return_value = mock_client_instance

        # Créer une instance de DBapi
        db_api = DBapi()
        db_api.client = mock_client_instance
        db_api.db = mock_client_instance['MangaTaMainDF']
        db_api.collection = mock_collection

        # Configurer le side_effect pour find
        def side_effect(query):
            submitted_range = query.get('submitted')
            return ['doc_submitted_{}'.format(i) for i in range(submitted_range['$gte'], submitted_range['$lt'])]
        mock_collection.find.side_effect = side_effect

        # Appeler la méthode
        result = db_api.find_range_submitted(1, 4)

        # Assertions
        expected_calls = [({'submitted': {'$gte': 1, '$lt': 4}},)]
        actual_calls = [call.args for call in mock_collection.find.call_args_list]
        assert actual_calls == expected_calls
        expected_result = ['doc_submitted_1', 'doc_submitted_2', 'doc_submitted_3']
        assert result == expected_result

def test_dbapi_use_query():
    with patch('src.dbapi.MongoClient') as mock_mongo_client:
        # Mock de la collection
        mock_collection = MagicMock()
        mock_db = {'Food.com': mock_collection}
        mock_client_instance = {'MangaTaMainDF': mock_db}
        mock_mongo_client.return_value = mock_client_instance

        # Créer une instance de DBapi
        db_api = DBapi()
        db_api.client = mock_client_instance
        db_api.db = mock_client_instance['MangaTaMainDF']
        db_api.collection = mock_collection

        # Configurer find()
        mock_collection.find.return_value = ['doc1', 'doc2']

        # Appeler la méthode avec une requête personnalisée
        query = {'field': 'value'}
        result = db_api.use_query(query)

        # Assertions
        mock_collection.find.assert_called_once_with(query)
        assert result == ['doc1', 'doc2']

def test_dbapi_close_connection():
    with patch('src.dbapi.MongoClient') as mock_mongo_client:
        # Mock du client
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        # Créer une instance de DBapi
        db_api = DBapi()
        db_api.client = mock_client_instance

        # Appeler close_connection
        db_api.close_connection()

        # Assertions
        mock_client_instance.close.assert_called_once()
