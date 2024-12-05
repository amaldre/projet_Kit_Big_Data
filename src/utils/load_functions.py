import pandas as pd
import os
import ast
from utils.dbapi import DBapi
import statsmodels.api as sm
import streamlit as st
import logging

logger = logging.getLogger(os.path.basename(__file__))


def load_csv(file_path):
    """
    Load a csv file from a given path and return a pandas dataframe

    :param file_path: The path to the csv file to load
    :type file_path: str
    :raises FileNotFoundError: If the file is not found
    :return: The loaded csv file as a pandas dataframe
    :rtype: pd.DataFrame
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def load_css(file_name):
    """
    Load a CSS file into the markdown file

    :param file_name: The name of the CSS file to load
    :type file_name: str
    """
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            logger.info(f"CSS charge avec succes depuis '{file_name}'.")
    except FileNotFoundError:
        error_message = f"Le fichier CSS '{file_name}' est introuvable."
        logger.error(error_message)
        st.error(error_message)
    except Exception as e:
        error_message = (
            f"Une erreur inattendue s'est produite lors du chargement du CSS : {e}"
        )
        logger.exception(error_message)
        st.error(error_message)


def transform_date_list(date_list):
    """
    Transform a list of dates in string format to a list of datetime objects


    :return: The list of dates as datetime objects
    :rtype: list
    """
    date_list = date_list.split(", ")[1:-2]
    return [pd.to_datetime(date) for date in date_list]


def load_df(file_path):
    """
    Load a csv file from a given path and return a pandas dataframe, change the columns to the correct type


    :param file_path: The path to the csv file to load
    :type file_path: str
    :return: The loaded csv file as a pandas dataframe
    :rtype: pd.DataFrame
    """
    df = load_csv(file_path)
    print(df.head())
    df["ingredients_replaced"] = df["ingredients_replaced"].apply(ast.literal_eval)
    df["ingredient_count"] = df["ingredients_replaced"].apply(len)
    df["techniques"] = df["techniques"].apply(ast.literal_eval)
    df["techniques_count"] = df["techniques"].apply(len)

    df["submitted"] = pd.to_datetime(df["submitted"])
    print(df["submitted"].dtype)

    return df


@st.cache_data
def load_data(PATH_DATA, file_name):
    path = os.path.join(PATH_DATA, file_name)
    try:
        if os.path.exists(path):
            logger.info(f"Chargement des donnees depuis {path}")
            return pd.read_csv(path)
        else:
            logger.warning(f"Fichier introuvable : {path}")
            return pd.DataFrame()  # Placeholder si le fichier est manquant
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier {file_name} : {e}")
        return pd.DataFrame()


@st.cache_data
def initialize_recipes_df(file_path):
    """
    Initialise le DataFrame dans l'etat de session de Streamlit.


    :param file_path: path to the CSV file
    :type file_path: str
    :return: The loaded csv file as a pandas dataframe
    :rtype: pd.DataFrame
    """

    try:
        dataframe = load_df(file_path)
        logger.info(f"DataFrame charge avec succes depuis '{file_path}'.")
        return dataframe
    except FileNotFoundError:
        error_message = f"Le fichier CSV '{file_path}' est introuvable."
        logger.error(error_message)
        st.error(error_message)
        dataframe = pd.DataFrame()  # Charger un DataFrame vide en cas d'erreur
        return dataframe
    except pd.errors.ParserError:
        error_message = (
            "Erreur lors du traitement du fichier CSV. Veuillez verifier son format."
        )
        logger.error(error_message)
        st.error(error_message)
        dataframe = pd.DataFrame()
        return dataframe
    except Exception as e:
        error_message = (
            f"Une erreur inattendue s'est produite lors du chargement du CSV : {e}"
        )
        logger.exception(error_message)
        st.error(error_message)
        dataframe = pd.DataFrame()
        return dataframe


def compute_trend(nb_recette_par_annee_df):
    """
    Compute the trend of the number of recipes submitted per month

    :param nb_recette_par_annee_df: The dataframe containing the number of recipes submitted per year
    :type nb_recette_par_annee_df: pd.DataFrame
    :return: The trend of the number of recipes submitted per month
    :rtype: pd.DataFrame
    """

    # nombre de recettes par années
    print(nb_recette_par_annee_df["submitted"].dtype)
    nb_recette_par_annee_df["year"] = nb_recette_par_annee_df["submitted"].dt.year
    nb_recette_par_annee_df["month"] = nb_recette_par_annee_df["submitted"].dt.month
    nb_recette_par_annee_df["submitted_by_month"] = (
        nb_recette_par_annee_df["submitted"].dt.to_period("M").dt.to_timestamp()
    )
    submissions_groupmonth = (
        nb_recette_par_annee_df["submitted_by_month"].value_counts().sort_index()
    )
    decomposition = sm.tsa.seasonal_decompose(
        submissions_groupmonth, model="additive", period=12
    )
    trend = pd.DataFrame(
        {
            "Date": decomposition.trend.index,  # X-axis: Time or index
            "Trend": decomposition.trend.values,  # Y-axis: Trend values
        }
    )
    return trend
