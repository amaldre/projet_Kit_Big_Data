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
    print(df.head())
    df["ingredients_replaced"] = df["ingredients_replaced"].apply(ast.literal_eval)
    print("1")
    df["ingredient_count"] = df["ingredients_replaced"].apply(len)
    print("2")
    df["submitted"] = pd.to_datetime(df["submitted"])
    print(df['submitted'].dtype)

    return df


# df = load_df("../data/processed_data.csv")

# print(df.columns)
# print(type(df["date"][0]))  # Devrait afficher <class 'list'>
# print(type(df["submitted"][0]))  # Devrait afficher <class 'Timestamp'>
# print(type(df["date"][0][0]))  # Devrait afficher <class 'Timestamp'>

# print(df["date"].head())S



def compute_trend(nb_recette_par_annee_df):


    # nombre de recettes par années
    print(nb_recette_par_annee_df['submitted'].dtype)
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