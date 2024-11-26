from pymongo import MongoClient, errors
import dotenv
import os
import logging

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

class DBapi:
    def __init__(self):
        self.client = None
        try:
            self.URI = os.getenv('URI_DB')
            if not self.URI:
                raise ValueError("URI_DB n'est pas défini dans les variables d'environnement.")
            self.client = MongoClient(self.URI)
            self.db = self.client["MangaTaMainDF"]
            self.collection = self.db["Food.com"]
            logging.info("Connexion à la base de données établie avec succès.")
        except errors.ConnectionError as e:
            logging.error(f"Erreur de connexion à la base de données : {e}")
        except Exception as e:
            logging.error(f"Une erreur est survenue : {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
    
    def find_by(self, colonne: str, value, nb=0):
        """
        Trouve des documents par colonne et valeur avec une limite optionnelle.
        """
        if self.client:
            try:
                cursor = self.collection.find({colonne : value})
                if nb > 0:
                    cursor = cursor.limit(nb)
                result = list(cursor)
                logging.info(f"{len(result)} documents trouvés pour {colonne} = {value}.")
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la recherche des documents : {e}")
        return []
    
    def find_range_submitted(self, begin, end):
        """
        Trouve des documents dont le champ 'submitted' est dans la plage donnée.
        """
        if self.client:
            try:
                query = {"submitted": {"$gte": begin, "$lt": end}}
                result = list(self.collection.find(query))
                logging.info(f"{len(result)} documents trouvés avec 'submitted' entre {begin} et {end}.")
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la recherche des documents : {e}")
        return []
    
    def use_query(self, query):
        """
        Exécute une requête personnalisée sur la collection.
        """
        if self.client:
            try:
                result = list(self.collection.find(query))
                logging.info(f"{len(result)} documents trouvés pour la requête personnalisée.")
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de l'exécution de la requête : {e}")
        return []
    
    def get_all_from(self, colonne: str):
        """
        Récupère toutes les données du champ spécifié 'colonne', en incluant 'recipe_id'.
        """
        if self.client:
            try:
                # Définir la projection pour inclure 'recipe_id' et 'colonne', exclure '_id'
                projection = {'_id': 0, 'recipe_id': 1, colonne: 1}
                cursor = self.collection.find({}, projection)
                result = list(cursor)
                logging.info(f"{len(result)} documents trouvés pour {colonne} avec 'recipe_id'.")
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la récupération des documents : {e}")
        return []

    def close_connection(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.client:
            self.client.close()
            self.client = None
            logging.info("Connexion à la base de données fermée.")
