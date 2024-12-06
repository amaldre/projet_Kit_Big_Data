"""
Page permettant de visualiser les donnees de maniere interactive.
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import date
from utils.bivariate_study import BivariateStudy
from utils.univariate_study import UnivariateStudy
import pandas as pd
import ast
from utils.load_functions import initialize_recipes_df, load_css
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

st.set_page_config(layout="wide")


# Charger le CSS
load_css("src/style.css")

st.title("DataViz")

st.markdown("Dans cette page, parcourez librement les donnees")

# Initialisation de la session
if "graph" not in st.session_state:
    st.session_state["graph"] = []

if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("data/cloud_df.csv")


def main():
    """
    Main function of the page DataViz. It allows to display and delete graphs.
    """
    # Definition des variables
    axis_x_list = [
        "calories",
        "minutes",
        "n_steps",
        "comment_count",
        "ingredient_count",
        "submitted",
    ]
    axis_y_list = ["comment_count", "mean_rating"]
    filters = ["comment_count", "mean_rating", "submitted"]
    axis_x_univar = [
        "calories",
        "ingredients_replaced",
        "techniques",
        "minutes",
        "n_steps",
        "comment_count",
        "ingredient_count",
        "submitted",
        "mean_rating",
    ]

    # Affichage des graphiques existants
    for i, graph in enumerate(st.session_state["graph"]):
        if graph.delete:
            st.session_state["graph"].remove(graph)
            logger.info(
                f"Graphique supprime. Nombre de graphiques restants: {len(st.session_state['graph'])}"
            )
        else:
            graph.display_graph(free=True)

    col1, col2 = st.columns(2)

    with col1:
        try:
            if st.button("Add univariate graph"):
                name = f"graph {len(st.session_state["graph"]) + 1}"
                study = UnivariateStudy(
                    dataframe=st.session_state["recipes_df"],
                    axis_x_list=axis_x_univar,
                    filters=filters,
                    key=name,
                    plot_type="density",
                )
                st.session_state["graph"].append(study)
                print("add", len(st.session_state["graph"]))
                st.rerun()
        except Exception as e:
            logger.error(
                f"Erreur lors de l'affichage ou de la suppression d'un graphique: {e}"
            )
            st.error(
                f"Une erreur est survenue lors de l'affichage ou de la suppression d'un graphique."
            )

    with col2:
        try:
            if st.button("Add bivariate graph"):
                name = f"graph {len(st.session_state["graph"]) + 1}"
                study = BivariateStudy(
                    dataframe=st.session_state["recipes_df"],
                    axis_x_list=axis_x_list,
                    axis_y_list=axis_y_list,
                    filters=filters,
                    key=name,
                    plot_type="scatter",
                )
                st.session_state["graph"].append(study)
                print("add", len(st.session_state["graph"]))
                st.rerun()
        except Exception as e:
            logger.error(
                f"Erreur lors de l'affichage ou de la suppression d'un graphique: {e}"
            )
            st.error(
                f"Une erreur est survenue lors de l'affichage ou de la suppression d'un graphique."
            )


if __name__ == "__main__":

    main()
