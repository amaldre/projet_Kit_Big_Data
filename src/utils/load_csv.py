import pandas as pd
import os
import ast
from utils.dbapi import DBapi
import statsmodels.api as sm

def load_csv(file_path):
    """
    Load a csv file from a given path and return a pandas dataframe
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def transform_date_list(date_list):
    """
    Transform a list of dates in string format to a list of datetime objects
    """
    date_list = date_list.split(", ")[1:-2]
    return [pd.to_datetime(date) for date in date_list]


def load_df(file_path):
    """
    Load a csv file from a given path and return a pandas dataframe, change the columns to the correct type
    """
    df = load_csv(file_path)

    df["tags"] = df["tags"].apply(ast.literal_eval)
    df["steps"] = df["steps"].apply(ast.literal_eval)
    df["ingredients"] = df["ingredients"].apply(ast.literal_eval)
    df["nutrition"] = df["nutrition"].apply(ast.literal_eval)
    df["techniques"] = df["techniques"].apply(ast.literal_eval)

    df["submitted"] = pd.to_datetime(df["submitted"]).dt.date
    df["date"] = df["date"].apply(transform_date_list)

    return df


# df = load_df("../data/processed_data.csv")

# print(df.columns)
# print(type(df["date"][0]))  # Devrait afficher <class 'list'>
# print(type(df["submitted"][0]))  # Devrait afficher <class 'Timestamp'>
# print(type(df["date"][0][0]))  # Devrait afficher <class 'Timestamp'>

# print(df["date"].head())S


def load_numerical_df():
    client_DB = DBapi()
    columns = ["recipe_id", "minutes", "submitted", "n_steps", "date", "rating", "ingredients_replaced", "cleaned_name"]
    numerical_df = client_DB.find_by_columns(columns)

    numerical_df['submitted'] = pd.to_datetime(numerical_df['submitted'])
    numerical_df['rating'] = numerical_df['rating'].apply(lambda x: ast.literal_eval(x))
    numerical_df['ingredients_replaced'] = numerical_df['ingredients_replaced'].apply(lambda x: ast.literal_eval(x))

    numerical_df['comment_count'] = numerical_df['rating'].apply(len)
    numerical_df['mean_rating'] = numerical_df['rating'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)
    numerical_df['ingredient_count'] = numerical_df['ingredients_replaced'].apply(len)

    numerical_df = numerical_df[["recipe_id",'mean_rating','comment_count',"minutes", "submitted", "n_steps", "date", "rating", "ingredients_replaced", "ingredient_count", "cleaned_name"]]

    return numerical_df


def load_trend():
    client_DB = DBapi()

    # nombre de recettes par années
    nb_recette_par_annee_df = client_DB.find_by_columns(["recipe_id", 'submitted','rating'])
    print(nb_recette_par_annee_df.head())
    nb_recette_par_annee_df['submitted'] = pd.to_datetime(nb_recette_par_annee_df['submitted'])
    nb_recette_par_annee_df['rating'] = nb_recette_par_annee_df['rating'].apply(lambda x: ast.literal_eval(x))

    nb_recette_par_annee_df['rating_count'] = nb_recette_par_annee_df['rating'].apply(len)
    nb_recette_par_annee_df['rating_mean'] = nb_recette_par_annee_df['rating'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)
    nb_recette_par_annee_df['year'] = nb_recette_par_annee_df['submitted'].dt.year
    nb_recette_par_annee_df['month'] = nb_recette_par_annee_df['submitted'].dt.month
    nb_recette_par_annee_df['submitted_by_month']=nb_recette_par_annee_df['submitted'].dt.to_period('M').dt.to_timestamp()
    submissions_groupmonth = nb_recette_par_annee_df['submitted_by_month'].value_counts().sort_index()
    decomposition = sm.tsa.seasonal_decompose(submissions_groupmonth, model='additive', period=12)
    trend = pd.DataFrame({
    'Date': decomposition.trend.index,   # X-axis: Time or index
    'Trend': decomposition.trend.values  # Y-axis: Trend values
    })
    return trend