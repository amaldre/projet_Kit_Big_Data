
from pymongo import MongoClient, errors
import dotenv
import os

dotenv.load_dotenv()

class DBapi:
    def __init__(self):
        try:
            self.URI = os.getenv('URI_DB')
            self.client = MongoClient(self.URI)
            self.db = self.client["MageTaMainDB"]
            self.collection = self.db["Food.com"]
        except errors.ConnectionError as e:
            print(f"Error connecting to database: {e}")
            self.client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def find_by(self, colonne: str, value, nb=0):
        """
        Find documents by column and value with an optional limit.
        """
        if self.client:
            try:
                return list(self.collection.find({colonne: value}).limit(nb))
            except errors.PyMongoError as e:
                print(f"Error finding documents: {e}")
                return []
        return []

    def find_range_submitted(self, begin, end):
        """
        Find documents with 'submitted' field in the given range.
        """
        if self.client:
            try:
                liste = []
                for i in range(begin, end, 1):
                    liste += list(self.collection.find({"submitted": i}))
                return liste
            except errors.PyMongoError as e:
                print(f"Error finding documents: {e}")
                return []
        return []

    def use_query(self, query):
        """
        Execute a custom query on the collection.
        """
        if self.client:
            try:
                return list(self.collection.find(query))
            except errors.PyMongoError as e:
                print(f"Error executing query: {e}")
                return []
        return []

    def close_connection(self):
        """
        Close the connection to the database.
        """
        if self.client:
            self.client.close()
