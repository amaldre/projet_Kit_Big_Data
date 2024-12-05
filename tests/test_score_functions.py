import pytest
import pandas as pd
from utils.score_functions import mean_score
from utils.score_functions import nb_reviews
from utils.score_functions import global_mean_score
from utils.score_functions import bayesian_average

def test_mean_score():
    database = pd.DataFrame({
        "recipe_id": [1, 1, 2],
        "rating": [3, 4, 5]
    })
    recipe_id = 1
    assert mean_score(recipe_id, database) == 3.5

def test_nb_reviews():
    database = pd.DataFrame({
        "recipe_id": [1, 1, 2],
        "rating": [3, 4, 5]
    })
    recipe_id = 1
    assert nb_reviews(recipe_id, database) == 2

def test_global_mean_score():
    database = pd.DataFrame({
        "recipe_id": [1, 1, 2],
        "rating": [3, 4, 5]
    })
    assert global_mean_score(database) == 4.0

def test_bayesian_average():
    r = 1
    v = 1
    c = 4
    m = 0
    assert bayesian_average(r, v, c, m) == 1.0