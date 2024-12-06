import sys
import os
from unittest.mock import patch, MagicMock
import pytest

# Ajouter le chemin au module utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.dbapi import DBApi


def test_dbapi_init():
    with patch("utils.dbapi.os.getenv") as mock_getenv, patch(
        "utils.dbapi.MongoClient"
    ) as mock_mongo_client:
        mock_getenv.return_value = "mongodb://localhost:27017"
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        db_api = DBApi()

        # Assertions
        mock_getenv.assert_called_once_with("URI_DB")
        mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")
        assert db_api.client == mock_client_instance
        assert db_api.db == mock_client_instance["MangaTaMainDF"]
        assert db_api.collection == db_api.db["Food.com"]


@patch("utils.dbapi.os.getenv")
def test_dbapi_find_by(mock_getenv):
    mock_getenv.return_value = "mongodb://mock_uri"
    with patch("utils.dbapi.MongoClient") as mock_mongo_client:
        mock_collection = MagicMock()
        mock_db = {"Food.com": mock_collection}
        mock_client_instance = {"MangaTaMainDF": mock_db}
        mock_mongo_client.return_value = mock_client_instance

        db_api = DBApi()

        db_api.client = mock_client_instance
        db_api.db = mock_client_instance["MangaTaMainDF"]
        db_api.collection = mock_collection

        # Configurer find().limit()
        mock_find = MagicMock()
        mock_collection.find.return_value = mock_find
        mock_find.limit.return_value = ["doc1", "doc2"]

        # Appeler la méthode
        result = db_api.find_by("test_col", "test_value", limit=2)

        # Assertions
        mock_collection.find.assert_called_once_with({"test_col": "test_value"})
        mock_find.limit.assert_called_once_with(2)
        assert result == ["doc1", "doc2"]


@patch("utils.dbapi.os.getenv")
def test_dbapi_find_range_submitted(mock_getenv):
    mock_getenv.return_value = "mongodb://mock_uri"
    with patch("utils.dbapi.MongoClient") as mock_mongo_client:
        # Mock de la collection
        mock_collection = MagicMock()
        mock_db = {"Food.com": mock_collection}
        mock_client_instance = {"MangaTaMainDF": mock_db}
        mock_mongo_client.return_value = mock_client_instance

        # Créer une instance de DBApi
        db_api = DBApi()
        db_api.client = mock_client_instance
        db_api.db = mock_client_instance["MangaTaMainDF"]
        db_api.collection = mock_collection

        # Configurer le side_effect pour find
        def side_effect(query):
            submitted_range = query.get("submitted")
            return [
                f"doc_submitted_{i}"
                for i in range(submitted_range["$gte"], submitted_range["$lt"])
            ]

        mock_collection.find.side_effect = side_effect

        # Appeler la méthode
        result = db_api.find_range_submitted(1, 4)

        # Assertions
        mock_collection.find.assert_called_once_with(
            {"submitted": {"$gte": 1, "$lt": 4}}
        )
        expected_result = ["doc_submitted_1", "doc_submitted_2", "doc_submitted_3"]
        assert result == expected_result


@patch("utils.dbapi.os.getenv")
def test_dbapi_close_connection(mock_getenv):
    mock_getenv.return_value = "mongodb://mock_uri"
    with patch("utils.dbapi.MongoClient") as mock_mongo_client:
        # Mock du client
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        # Créer une instance de DBApi
        db_api = DBApi()
        db_api.client = mock_client_instance

        # Appeler close_connection
        db_api.close_connection()

        # Assertions
        mock_client_instance.close.assert_called_once()
