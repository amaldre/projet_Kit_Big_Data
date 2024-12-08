"""
Ce module fournit des fonctions pour calculer des scores liés aux évaluations des recettes.
"""


def mean_score(recipe_id, database):
    """
    Calcule la moyenne des notes pour une recette donnée.

    :param recipe_id: L'identifiant unique de la recette.
    :type recipe_id: int
    :param database: Le DataFrame contenant les évaluations des recettes.
    :type database: pandas.DataFrame
    :return: La moyenne des notes pour la recette spécifiée.
    :rtype: float
    """
    return database[database["recipe_id"] == recipe_id]["rating"].mean()


def nb_reviews(recipe_id, database):
    """
    Calcule le nombre de critiques pour une recette donnée.

    :param recipe_id: L'identifiant unique de la recette.
    :type recipe_id: int
    :param database: Le DataFrame contenant les évaluations des recettes.
    :type database: pandas.DataFrame
    :return: Le nombre d'évaluations pour la recette spécifiée.
    :rtype: int
    """
    return database[database["recipe_id"] == recipe_id].shape[0]


def global_mean_score(database):
    """
    Calcule la moyenne globale des notes sur l'ensemble des recettes.

    :param database: Le DataFrame contenant les évaluations des recettes.
    :type database: pandas.DataFrame
    :return: La moyenne globale des notes.
    :rtype: float
    """
    return database["rating"].mean()


def bayesian_average(r, v, c, m=5):
    """
    Calcule le score bayésien moyen pour une recette donnée.

    Cette méthode prend en compte la moyenne des notes, le nombre d'évaluations,
    et la moyenne globale pour produire un score équilibré.

    :param r: Moyenne des notes pour une recette.
    :type r: float
    :param v: Nombre d'évaluations pour cette recette.
    :type v: int
    :param c: Moyenne globale des notes sur l'ensemble du dataset.
    :type c: float
    :param m: Seuil minimum de votes requis pour qu'un item soit considéré pertinent (par défaut 5).
    :type m: int, optional
    :return: Le score bayésien moyen pour la recette.
    :rtype: float
    """
    return (r * v / (v + m)) + (c * m / (v + m))
