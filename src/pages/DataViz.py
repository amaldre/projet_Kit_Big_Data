import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import date
from utils.classes import bivariateStudy
import ast
from utils.load_csv import load_df
import logging
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
        st.error(f"Une erreur est survenue lors du chargement du fichier CSS. Veuillez verifier le fichier.")

# Charger le CSS
load_css("style.css")

st.title("DataViz")

st.markdown("Dans cette page, parcourez librement les donnees")

# Initialisation de la session
if "graph" not in st.session_state:
    st.session_state["graph"] = []

if "recipes_df" not in st.session_state:
    try:
        st.session_state["recipes_df"] = load_df("data/cloud_df.csv")
        logger.info("Les donnees de recettes ont ete chargees avec succes.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des donnees depuis le fichier CSV: {e}")
        st.error("Une erreur est survenue lors du chargement des donnees. Veuillez verifier le fichier.")

def main():
    # Definition des variables
    axis_x_list = [
        "minutes",
        "n_steps",
        "comments_count",
        "ingredient_count",
        "submitted",
    ]
    axis_y_list = ["comment_count", "mean_rating"]
    filters = ["comment_count", "mean_rating", "submitted"]

    # Affichage des graphiques existants
    for i, graph in enumerate(st.session_state["graph"]):
        try:
            if graph.delete:
                st.session_state["graph"].remove(graph)
                logger.info(f"Graphique supprime. Nombre de graphiques restants: {len(st.session_state['graph'])}")
            else:
                graph.display_graph(free=True)
        except Exception as e:
            logger.error(f"Erreur lors de l'affichage ou de la suppression d'un graphique: {e}")
            st.error(f"Une erreur est survenue lors de l'affichage ou de la suppression d'un graphique.")

    # Ajout d'un graphique
    if st.button("Add Graph"):
        try:
            name = f"graph {len(st.session_state['graph']) + 1}"
            study = bivariateStudy(dataframe=st.session_state["recipes_df"], axis_x_list=axis_x_list, axis_y_list=axis_y_list, filters=filters, key=name, plot_type="scatter")
            st.session_state["graph"].append(study)
            logger.info(f"Graphique ajoute. Nombre de graphiques actuels: {len(st.session_state['graph'])}")
            st.rerun()
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'un graphique: {e}")
            st.error(f"Une erreur est survenue lors de l'ajout du graphique.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Erreur critique dans l'execution de l'application: {e}")
        st.error("Une erreur critique est survenue dans l'application.")
