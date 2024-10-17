def mean_score(recipe_id, database): 
    return database[database['recipe_id'] == recipe_id]["rating"].mean()

def nb_reviews(recipe_id, database):
    return database[database["recipe_id"] == recipe_id].shape[0]

def global_mean_score(database):
    return database["rating"].mean()

def bayesian_average(r,v,c,m=5): #score function that takes into account the number of reviews
    return (r*v/(v+m))+(c*m/(v+m))
"""
r = Moyenne des notes pour une recette.
v = Nombre d'évaluations pour cette recette.
c = Moyenne globale des notes sur l'ensemble du dataset.
m = Seuil minimum de votes requis pour qu'un item soit considéré pertinent (une constante que vous définissez).
"""