"""
Ce module contient des fonctions pour charger des fichiers, manipuler des données et calculer des tendances.
"""

import os
import ast
import logging
import pandas as pd
import statsmodels.api as sm
import streamlit as st
import base64 

logger = logging.getLogger(os.path.basename(__file__))


def load_csv(file_path):
    """
    Charge un fichier CSV depuis un chemin donné et retourne un DataFrame pandas.

    :param file_path: Le chemin du fichier CSV à charger.
    :type file_path: str
    :raises FileNotFoundError: Si le fichier n'est pas trouvé.
    :return: Le fichier CSV chargé sous forme de DataFrame pandas.
    :rtype: pd.DataFrame
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

@st.cache_data
def load_css(file_name):
    """
    Charge un fichier CSS et l'applique à la page Streamlit.

    :param file_name: Le nom du fichier CSS à charger.
    :type file_name: str
    """
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            logger.info("CSS chargé avec succès depuis '%s'.", file_name)
        load_background()
    except FileNotFoundError:
        error_message = f"Le fichier CSS '{file_name}' est introuvable."
        logger.error(error_message)
        st.error(error_message)
    except Exception as e:
        logger.exception(
            "Une erreur inattendue s'est produite lors du chargement du CSS : %s", e
        )
        st.error(f"Une erreur inattendue s'est produite : {e}")

def load_background():
    with open("images/background.png", "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode()
    page_bg_img = f'''
    <style>
    .stSidebar {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        
    }}
    .stSidebar::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.80);  /* Semi-transparent white overlay */
    }}
    <style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return True


def load_df(file_path):
    """
    Charge un fichier CSV, applique des transformations
    sur les colonnes et retourne un DataFrame pandas.

    :param file_path: Le chemin du fichier CSV à charger.
    :type file_path: str
    :return: Le fichier CSV transformé sous forme de DataFrame pandas.
    :rtype: pd.DataFrame
    """
    df = load_csv(file_path)
    df["Ingrédients"] = df["Ingrédients"].apply(ast.literal_eval)
    df["Nombre d'ingrédients"] = df["Ingrédients"].apply(len)
    df["Techniques utilisées"] = df["Techniques utilisées"].apply(ast.literal_eval)
    df["Nombre de techniques utilisées"] = df["Techniques utilisées"].apply(len)
    df["Date de publication de la recette"] = pd.to_datetime(df["Date de publication de la recette"])
    return df


@st.cache_data
def load_data(path_data, file_name):
    """
    Charge un fichier CSV depuis un chemin donné.

    :param path_data: Le chemin du dossier contenant le fichier.
    :type path_data: str
    :param file_name: Le nom du fichier CSV à charger.
    :type file_name: str
    :return: Un DataFrame pandas contenant les données
    ou un DataFrame vide si le fichier est introuvable.
    :rtype: pd.DataFrame
    """
    path = os.path.join(path_data, file_name)
    try:
        if os.path.exists(path):
            logger.info("Chargement des données depuis %s", path)
            return pd.read_csv(path)
        logger.warning("Fichier introuvable : %s", path)
        return pd.DataFrame()  # Placeholder si le fichier est manquant
    except Exception as e:
        logger.error("Erreur lors du chargement du fichier %s : %s", file_name, e)
        return pd.DataFrame()


@st.cache_data
def initialize_recipes_df(file_path):
    """
    Initialise un DataFrame à partir d'un fichier CSV.

    :param file_path: Chemin vers le fichier CSV.
    :type file_path: str
    :return: Le DataFrame chargé ou un DataFrame vide en cas d'erreur.
    :rtype: pd.DataFrame
    """
    try:
        dataframe = load_df(file_path)
        logger.info("DataFrame chargé avec succès depuis '%s'.", file_path)
        return dataframe
    except FileNotFoundError:
        error_message = f"Le fichier CSV '{file_path}' est introuvable."
        logger.error(error_message)
        st.error(error_message)
        return pd.DataFrame()  # DataFrame vide en cas d'erreur
    except pd.errors.ParserError:
        error_message = (
            "Erreur lors du traitement du fichier CSV. Veuillez vérifier son format."
        )
        logger.error(error_message)
        st.error(error_message)
        return pd.DataFrame()
    except Exception as e:
        logger.exception(
            "Une erreur inattendue s'est produite lors du chargement du CSV : %s", e
        )
        st.error(f"Une erreur inattendue s'est produite : {e}")
        return pd.DataFrame()


def compute_trend(nb_recette_par_annee_df):
    """
    Calcule la tendance du nombre de recettes soumises par mois.

    :param nb_recette_par_annee_df: DataFrame contenant les données des recettes soumises.
    :type nb_recette_par_annee_df: pd.DataFrame
    :return: Un DataFrame contenant les tendances calculées
    ou un DataFrame vide si les données sont insuffisantes.
    :rtype: pd.DataFrame
    """
    if nb_recette_par_annee_df.empty:
        return pd.DataFrame()

    if "Date de publication de la recette" in nb_recette_par_annee_df.columns:
        nb_recette_par_annee_df["Date de publication de la recette"] = pd.to_datetime(
            nb_recette_par_annee_df["Date de publication de la recette"], errors="coerce"
        )

    if nb_recette_par_annee_df["Date de publication de la recette"].isnull().all():
        return pd.DataFrame()

    nb_recette_par_annee_df["year"] = nb_recette_par_annee_df["Date de publication de la recette"].dt.year
    nb_recette_par_annee_df["month"] = nb_recette_par_annee_df["Date de publication de la recette"].dt.month
    nb_recette_par_annee_df["submitted_by_month"] = (
        nb_recette_par_annee_df["Date de publication de la recette"].dt.to_period("M").dt.to_timestamp()
    )
    submissions_groupmonth = (
        nb_recette_par_annee_df["submitted_by_month"].value_counts().sort_index()
    )

    if len(submissions_groupmonth) < 12:
        return pd.DataFrame()

    decomposition = sm.tsa.seasonal_decompose(
        submissions_groupmonth, model="additive", period=12
    )
    trend = pd.DataFrame(
        {
            "Date": decomposition.trend.index,  # X-axis: Time or index
            "Moyenne glissante": decomposition.trend.values,  # Y-axis: Trend values
        }
    )
    return trend
