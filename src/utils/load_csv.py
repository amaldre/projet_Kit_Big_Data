import pandas as pd
import os
import ast


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


df = load_df("../data/processed_data.csv")

print(df.columns)
print(type(df["date"][0]))  # Devrait afficher <class 'list'>
print(type(df["submitted"][0]))  # Devrait afficher <class 'Timestamp'>
print(type(df["date"][0][0]))  # Devrait afficher <class 'Timestamp'>

print(df["date"].head())
