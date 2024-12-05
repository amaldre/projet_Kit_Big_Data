import pandas as pd
import numpy as np
import os
import ast
import nltk
import re
from datetime import date


def load_nltk_resources():
    """
    Load the nltk resources
    """
    nltk.download("punkt_tab")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("wordnet")
    nltk.download("stopwords")


PATH_DATA = "../data/"
RAW_RECIPE = "RAW_recipes.csv"
RAW_INTERACTIONS = "RAW_interactions.csv"
PROCESSED_DATA = "processed_data.csv"
PROCESSED_DATA_JSON = "processed_data.json"
PP_RECIPES = "PP_recipes.csv"


def load_data(path: str):
    """Load the data from the path

    Args:
        path (str): The path of the data

    Returns:
        df : The data in a pandas dataframe
    """
    data = pd.read_csv(path)
    return data


def change_to_date_time_format(data: pd, colone: str):
    """
    Change the column to datetime format

    Args:
        data (pd): The data in a pandas dataframe
        colone (str): The column to change to datetime format

    Returns:
        data : The data in a pandas dataframe with the column in datetime format
    """

    data[colone] = pd.to_datetime(data[colone], format="%Y-%m-%d").dt.date
    return data


def change_to_list(data: pd, colone: str):
    """Change the column to a list of strings

    Args:
        data (pd): Data in a pandas dataframe
        colone (str): The column to change to a list of strings

    Returns:
        panda df : The data in a pandas dataframe with the column as a list of strings
    """
    data[colone] = data[colone].apply(ast.literal_eval)
    print("Type après conversion:", type(data[colone].iloc[0]))
    return data


def change_to_str(data: pd, colone: str):
    """Change the column to a string

    Args:
        data (pd): Data in a pandas dataframe
        colone (str): Column to change to a string

    Returns:
        df : The data in a pandas dataframe with the column as a string
    """
    if data[colone].dtype == list:
        data[colone] = data[colone].apply(lambda x: " ".join(x))
    else:
        data[colone] = data[colone].apply(str)
    return data


def change_category(data: pd, colone: str):
    data[colone] = data[colone].astype("category")
    return data


def merge_dataframe(dataframe1, dataframe2, lefton, righton):
    data = pd.merge(dataframe1, dataframe2, left_on=lefton, right_on=righton)
    return data


def groupby(data: pd):
    """ "
    Group the data by recipe_id and aggregate the columns from Interactions as List

    Args:
        data (pd): The data in a pandas dataframe

    Returns:
        df : The data in a pandas dataframe grouped by recipe_id
    """
    df = (
        data.groupby(["recipe_id"])
        .agg(
            {
                "i": "first",
                "name_tokens": "first",
                "ingredient_tokens": "first",
                "steps_tokens": "first",
                "techniques": "first",
                "calorie_level": "first",
                "ingredient_ids": "first",
                "name": "first",
                "minutes": "first",
                "contributor_id": "first",
                "submitted": "first",
                "tags": "first",
                "nutrition": "first",
                "steps": "first",
                "n_steps": "first",
                "description": "first",
                "ingredients": "first",
                "n_ingredients": "first",
                "review": lambda x: list(x) if len(x) > 0 else [],
                "date": lambda x: list(x) if len(x) > 0 else [],
                "user_id": lambda x: list(x) if len(x) > 0 else [],
                "rating": lambda x: list(x) if len(x) > 0 else [],
            }
        )
        .reset_index()
    )

    return df


def change_na_description_by_name(data: pd):
    """ "
    Change the description column by the name column
    if the name is not null, otherwise drop the row
    """

    data["description"] = data["description"].fillna(data["name"])
    data = data.dropna(subset=["name"])
    return data


def delete_outliers_minutes(data: pd):
    """ "
    Delete the two largest minutes (troll recipes)
    Delete Recipe with 0 minutes

    Args:
        data (pd): The data in a pandas dataframe

    Returns:
        df : The data in a pandas dataframe without the two largest minutes and 0 minutes' recipes

    """
    data = data.drop(data["minutes"].nlargest(2).index)
    data = data[data["minutes"] != 0]
    return data


def delete_outliers_calories(data: pd):
    """Delete Recipe over 300 000 calories (outliers)

    :param data: dataframe des recettes
    :type data: pd
    :return: dataframe des recettes sans les recettes avec plus de 300 000 calories
    :rtype: pd.dataframe
    """
    data = data[data["calories"] > 300000]
    return data


def delete_outliers_steps(data: pd):
    """ "
    Delete Recipe with 0 steps

    Args:
        data (pd): The data in a pandas dataframe

    Returns:
        df : The data in a pandas dataframe without and 0 steps' recipes

    """
    data = data[data["n_steps"] != 0]
    return data


def get_stopwords():
    """
    Get the stopwords from nltk

    Returns:
        stopwords : The stopwords from nltk aggregated with custom stopwords
    """

    nltk.download("stopwords")

    custom_stopwords = {
        "recipe",
        "recipes",
        "time",
        "one",
        "like",
        "use",
        "from",
        "make",
        "made",
        "used",
        "dont",
        "well",
        "really",
        "came",
        "with",
        "get",
        "found",
        "find",
        "ii",
        "try",
        "tried",
        "also",
        "add",
        "got",
    }

    stopwords = set(nltk.corpus.stopwords.words("english")) | custom_stopwords
    return stopwords


def clean_and_tokenize(text: str, stopwords: set, do_pos_tags=True):
    """
    Clean and tokenize the text by removing stopwords and punctuation. Filtered also the POS tags to keep only the nouns and verbs

    Args:
        text (_type_): _description_

    Returns:
        str: _description_
    """
    text = text.lower()
    text = re.sub(r"[0-9]+", "", text)
    text = re.sub(r"[.;:!\'?,\"()\[\]]", "", text)

    tokens = nltk.word_tokenize(text)

    if do_pos_tags:
        pos_tags = nltk.pos_tag(tokens)

    filtered_tokens = [
        word
        for word, tag in pos_tags
        if tag
        not in (
            "JJ",
            "JJR",
            "JJS",  # Adjectifs
            "DT",  # Déterminants
            "PRP",
            "PRP$",
            "WP",
            "WP$",  # Pronoms
            "RB",
            "RBR",
            "RBS",  # Adverbes
            "MD",  # Modaux
            "VB",
            "VBD",
            "VBG",
            "VBN",
            "VBP",
            "VBZ",  # Tous les types de verbes
            "CC",
            "IN",  # Conjonctions et prépositions
            "CD",  # Nombres
            "UH",  # Interjections
        )
    ]
    filtered_tokens = [
        word for word in filtered_tokens if word.lower() not in stopwords
    ]

    return filtered_tokens


def clean_colonne(data: pd, colonne: str, stopwords: set):
    """
    Clean the column by removing stopwords and punctuation. Filtered also the POS tags to keep only the nouns and verbs

    Args:
        data (pd): The data in a pandas dataframe
        colonne (str): The column to clean
        stopwords (set): The stopwords to remove

    Returns:
        df : The data in a pandas dataframe with the column cleaned
    """
    data["cleaned_" + colonne] = data[colonne].apply(
        lambda x: clean_and_tokenize(x, stopwords)
    )
    return data


def ingredient_to_ingredient_processed(
    ingredient_list: list, processed_dict: dict, replaced_dict: dict
):
    """
    From an list of ingredients, get the name of the processed ingredient and the name of the replaced ingredient

    Args:
        ingredient_list (list): The ingredient
        processed_dict (dict): The dictionary of processed ingredients
        replaced_dict (dict): The dictionary of replaced ingredients

    Returns:
        processed_list : The processed ingredient
        replaced_list : The replaced ingredient
    """

    processed_list = [
        processed_dict.get(ingredient, None) for ingredient in ingredient_list
    ]
    replaced_list = [
        replaced_dict.get(ingredient, None) for ingredient in ingredient_list
    ]
    return processed_list, replaced_list


def processed_ingredient(data: pd):
    """
    Process the ingredients by removing stopwords and punctuation. Filtered also the POS tags to keep only the nouns and verbs

    Args:
        data (pd): The data in a pandas dataframe

    Returns:
        df : The data in a pandas dataframe with the ingredients processed and replaced
    """
    ingredients_data = load_data(os.path.join(PATH_DATA, "ingredients.csv"))

    processed_dict = ingredients_data.set_index("raw_ingr")["processed"].to_dict()
    replaced_dict = ingredients_data.set_index("raw_ingr")["replaced"].to_dict()

    data[["ingredients_processed", "ingredients_replaced"]] = (
        data["ingredients"]
        .apply(
            lambda x: ingredient_to_ingredient_processed(
                x, processed_dict, replaced_dict
            )
        )
        .apply(pd.Series)
    )
    return data


def delete_unwanted_columns(data: pd, columns: list):
    """Delete the unwanted columns

    :param data: The data in a pandas dataframe
    :type data: pd
    :param columns: list of columns to delete
    :type columns: list

    :return: The data in a pandas dataframe without the unwanted columns
    :rtype: pd.dataframe
    """
    data.drop(columns, axis=1, inplace=True)
    return data


def save_data(data: pd, path: str):
    """Save the data to the path

    Args:
        data (pd): Data in a pandas dataframe
        path (str): The path to save the data
    """
    data.to_csv(path, index=False)


def save_data_json(data: pd, path: str):
    """Save the data to the path in json format

    Args:
        data (pd): Data in a pandas dataframe
        path (str): The path to save the data
    """
    data.to_json(path, orient="records", lines=True)


def preprocess():
    """
    Preprocess the data by loading, cleaning, and saving it
    """

    print("Downloading nltk resources")
    load_nltk_resources()

    raw_recipe_data = load_data(os.path.join(PATH_DATA, RAW_RECIPE))
    raw_interactions_data = load_data(os.path.join(PATH_DATA, RAW_INTERACTIONS))
    pp_recipes_data = load_data(os.path.join(PATH_DATA, PP_RECIPES))

    raw_recipe_data = change_to_date_time_format(raw_recipe_data, "submitted")
    raw_interactions_data = change_to_date_time_format(raw_interactions_data, "date")

    raw_recipe_data = change_to_list(raw_recipe_data, "tags")
    raw_recipe_data = change_to_list(raw_recipe_data, "steps")
    raw_recipe_data = change_to_list(raw_recipe_data, "nutrition")
    raw_recipe_data = change_to_list(raw_recipe_data, "ingredients")
    pp_recipes_data = change_to_list(pp_recipes_data, "techniques")

    df = merge_dataframe(raw_recipe_data, raw_interactions_data, "id", "recipe_id")
    print("Type après merge:", type(df["ingredients"].iloc[0]))
    df = merge_dataframe(pp_recipes_data, df, "id", "recipe_id")
    df = groupby(df)

    df = change_na_description_by_name(df)

    df = change_category(df, "contributor_id")
    df = change_category(df, "recipe_id")

    df = delete_outliers_minutes(df)
    df = delete_outliers_steps(df)
    df = delete_outliers_calories(df)

    stopwords = get_stopwords()
    df = clean_colonne(df, "description", stopwords)
    df = clean_colonne(df, "name", stopwords)

    df = processed_ingredient(df)

    # supression des colonnes inutiles
    unwated_columns = [
        "i",
        "name_tokens",
        "ingredient_tokens",
        "steps_tokens",
        "techniques",
        "ingredient_ids",
        "tags",
        "nutrition",
        "steps",
        "ingredients",
    ]
    df = delete_unwanted_columns(df, unwated_columns)

    save_data(df, os.path.join(PATH_DATA, PROCESSED_DATA))
    save_data_json(df, os.path.join(PATH_DATA, PROCESSED_DATA_JSON))


# preprocess()
