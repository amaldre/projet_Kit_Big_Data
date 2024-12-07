"""
Ce fichier sert  à configurer la page d'accueil de l'application Streamlit.
"""

import os
import streamlit as st
import pandas as pd
import logging
from logging_config import setup_logging
from utils.load_functions import initialize_recipes_df, load_css

st.set_page_config(layout="wide")

# Initialiser le logger
setup_logging()  # Configuration
logger = logging.getLogger(os.path.basename(__file__))


# Charger les styles CSS
load_css("src/style.css")

# Initialiser les donnees dans l'etat de session
if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("data/clean_cloud_df.csv")


def main():
    # Configuration de l'application Streamlit
    st.title("Mange ta main")

    st.markdown(
        """
        Bienvenue sur cette application web ! Elle a pour but de proposer une analyse interactive 
        des données du site **Mangetamain**, ancien leader dans la recommandation B2C de recettes 
        de cuisine à l'ancienne bio. L'analyse porte sur des données récoltées entre **1999 et 2018** et 
        vise à expliquer les clés qui ont fait le succès de Mangetamain, tout en proposant des pistes 
        pour lui faire regagner en popularité.

        ### Sections de l'application :
        1. **Analyse des données** : Graphiques principaux pour comprendre les éléments clés de l'analyse.
        2. **Clustering** : Analyse approfondie des données de recettes grâce au clustering.
        3. **Dataviz** : Créez vos propres graphiques à partir des données.
        4. **Preprocessing** : Détails sur les méthodes utilisées dans l'analyse.
        5. **Carte** : Un exemple fictif d'analyse géographique.
        """
    )

    # Embed CSS for the wave animation
    st.markdown(
        """
      <style>
      @keyframes wave {
        0% {
          transform: translateX(-100%);
        }
        100% {
          transform: translateX(100%);
        }
      }

      .wave-container {
        position: fixed;
        top: 50%;
        left: 0;
        width: 100%;
        height: 20px;
        overflow: hidden;
        z-index: 9999;
      }

      .wave {
        position: absolute;
        width: 200%;
        height: 100%;
        background: linear-gradient(to right, #3498db, #8e44ad);
        animation: wave 4s linear infinite;
        opacity: 0.5;
        border-radius: 50%;
      }
      </style>
      <div class="wave-container">
        <div class="wave"></div>
      </div>
      """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
