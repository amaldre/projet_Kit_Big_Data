import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import time
from collections import Counter
import logging
from utils.univariateStudy import univariateStudy
from utils.classes import AdvancedStudy
from utils.load_csv import load_df
import os

logger = logging.getLogger(os.path.basename(__file__))

st.set_page_config(layout="wide")


def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        logger.info(f"Le fichier CSS {file_name} a ete charge avec succes.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier CSS {file_name}: {e}")
        st.error(
            f"Une erreur est survenue lors du chargement du fichier CSS. Veuillez verifier le fichier."
        )


# Charger le fichier CSS
load_css("style.css")

st.title("Data Visualiser")


@st.cache_data
def import_df(df_path):
    try:
        recipes_df = pd.read_csv(df_path)
        logger.info(f"Les donnees ont ete importees depuis {df_path} avec succes.")
        return recipes_df
    except Exception as e:
        logger.error(f"Erreur lors de l'importation des donnees depuis {df_path}: {e}")
        st.error(
            "Une erreur est survenue lors de l'importation des donnees. Veuillez verifier le fichier."
        )
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur


# Initialisation des etats de session
if "graph_advanced" not in st.session_state:
    st.session_state["graph_advanced"] = []

if "filters_advanced" not in st.session_state:
    st.session_state["filters_advanced"] = []

if "recipes_df" not in st.session_state:
    try:
        st.session_state["recipes_df"] = load_df("data/cloud_df.csv")
        logger.info("Les donnees de recettes ont ete chargees avec succes.")
    except Exception as e:
        logger.error(
            f"Erreur lors du chargement des donnees depuis le fichier CSV: {e}"
        )
        st.error(
            "Une erreur est survenue lors du chargement des donnees. Veuillez verifier le fichier."
        )
        st.session_state["recipes_df"] = (
            pd.DataFrame()
        )  # Retourner un DataFrame vide en cas d'erreur


def main():
    # Creation des colonnes pour les boutons
    col1, col2, _, _, _, _, _, _, _, _ = st.columns(10)

    with col1:
        refresh_button = st.button("refresh")
    with col2:
        add_graph_button = st.button("Add Graph")

    # Bouton refresh
    if refresh_button:
        logger.info("Bouton refresh clique. Redemarrage de l'application.")
        st.rerun()

    axis_x_list = [
        "calories",
        "mean_rating",
        "comment_count",
        "n_steps",
        "ingredients_replaced",
        "techniques",
        "ingredients_by_year",
    ]
    filters = ["calories", "mean_rating", "comment_count", "n_steps"]

    # Bouton pour ajouter un graphique
    if add_graph_button:
        try:
            name = f"{len(st.session_state['graph_advanced']) + 1}"
            study = AdvancedStudy(
                st.session_state["recipes_df"],
                axis_x=None,
                axis_x_list=axis_x_list,
                filters=filters,
                key=name,
            )
            st.session_state["graph_advanced"].append(study)
            logger.info(
                f"Graphique ajoute avec le nom: {name}. Nombre total de graphiques: {len(st.session_state['graph_advanced'])}."
            )
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'un graphique: {e}")
            st.error("Une erreur est survenue lors de l'ajout d'un graphique.")

    # Affichage des graphiques existants
    for i, graph in enumerate(st.session_state["graph_advanced"]):
        try:
            if graph.delete:
                st.session_state["graph_advanced"].remove(graph)
                logger.info(
                    f"Graphique supprime. Nombre restant de graphiques: {len(st.session_state['graph_advanced'])}."
                )
            else:
                graph.display_graph()
        except Exception as e:
            logger.error(
                f"Erreur lors de l'affichage ou de la suppression d'un graphique: {e}"
            )
            st.error(
                "Une erreur est survenue lors de l'affichage ou de la suppression d'un graphique."
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Erreur critique dans l'execution de l'application: {e}")
        st.error("Une erreur critique est survenue dans l'application.")
