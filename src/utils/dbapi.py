""" 
Module pour interagir avec une base de données MongoDB. 
"""

import os
import logging
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import pandas as pd

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)


class DBApi:
    """
    Classe pour interagir avec une base de données MongoDB.
    """

    def __init__(self):
        """
        Initialise la connexion à la base de données MongoDB.
        """
        self.client = None
        self.uri = os.getenv("URI_DB")
        if not self.uri:
            raise ValueError(
                "URI_DB n'est pas défini dans les variables d'environnement."
            )
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client["MangaTaMainDF"]
            self.collection = self.db["Food.com"]
            logging.info("Connexion à la base de données établie avec succès.")
        except errors.ConfigurationError as config_error:
            logging.error("Erreur de connexion à la base de données : %s", config_error)
        except Exception as generic_error:
            logging.error("Une erreur est survenue : %s", generic_error)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def find_by(self, column: str, value, limit=0):
        """
        Trouve des documents par colonne et valeur avec une limite optionnelle.

        :param column: Colonne sur laquelle filtrer.
        :param value: Valeur à rechercher.
        :param limit: Nombre maximum de documents à récupérer.
        :return: Liste des documents correspondants.
        """
        if not self.client:
            return []

        try:
            cursor = self.collection.find({column: value})
            if limit > 0:
                cursor = cursor.limit(limit)
            result = list(cursor)
            logging.info(
                "%d documents trouvés pour %s = %s.", len(result), column, value
            )
            return result
        except errors.PyMongoError as pymongo_error:
            logging.error(
                "Erreur lors de la recherche des documents : %s", pymongo_error
            )
            return []

    def find_by_columns(self, columns: list, limit=0):
        """
        Trouve des documents en spécifiant les colonnes à inclure.

        :param columns: Liste des colonnes à inclure dans le résultat.
        :param limit: Nombre maximum de documents à récupérer.
        :return: DataFrame des documents correspondants.
        """
        if not self.client:
            return pd.DataFrame()

        try:
            projection = {col: 1 for col in columns}
            projection["_id"] = 0
            cursor = self.collection.find({}, projection).limit(limit)
            return pd.DataFrame(list(cursor))
        except errors.PyMongoError as pymongo_error:
            logging.error(
                "Erreur lors de la recherche des documents : %s", pymongo_error
            )
            return pd.DataFrame()

    def find_range_submitted(self, begin, end):
        """
        Trouve des documents dont le champ 'submitted' est dans la plage donnée.

        :param begin: Date de début.
        :param end: Date de fin.
        :return: Liste des documents correspondants.
        """
        if not self.client:
            return []

        try:
            query = {"submitted": {"$gte": begin, "$lt": end}}
            result = list(self.collection.find(query))
            logging.info(
                "%d documents trouvés avec 'submitted' entre %s et %s.",
                len(result),
                begin,
                end,
            )
            return result
        except errors.PyMongoError as pymongo_error:
            logging.error(
                "Erreur lors de la recherche des documents : %s", pymongo_error
            )
            return []

    def get_all_from(self, column: str):
        """
        Récupère toutes les données pour une colonne donnée.

        :param column: Nom de la colonne.
        :return: Liste des documents correspondants.
        """
        if not self.client:
            return []

        try:
            projection = {"_id": 0, "recipe_id": 1, column: 1}
            result = list(self.collection.find({}, projection))
            logging.info(
                "%d documents trouvés pour %s avec 'recipe_id'.", len(result), column
            )
            return result
        except errors.PyMongoError as pymongo_error:
            logging.error(
                "Erreur lors de la récupération des documents : %s", pymongo_error
            )
            return []

    def get_percentage_documents(self, columns=None, percentage=1):
        """
        Renvoie un pourcentage de documents aléatoires avec les colonnes spécifiées.

        :param columns: Liste des colonnes à inclure.
        :param percentage: Pourcentage des documents à renvoyer (entre 0 et 1).
        :return: Liste des documents correspondants.
        """
        if not self.client:
            return []

        try:
            projection = {"_id": 0}
            if columns:
                projection.update({col: 1 for col in columns})

            sample_size = int(percentage * self.collection.count_documents({}))
            cursor = self.collection.aggregate(
                [{"$sample": {"size": sample_size}}, {"$project": projection}]
            )
            result = list(cursor)
            logging.info(
                "%d documents récupérés avec un pourcentage de %s.",
                len(result),
                percentage,
            )
            return result
        except errors.PyMongoError as pymongo_error:
            logging.error(
                "Erreur lors de la récupération des documents : %s", pymongo_error
            )
            return []

    def close_connection(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.client:
            self.client.close()
            self.client = None
            logging.info("Connexion à la base de données fermée.")
