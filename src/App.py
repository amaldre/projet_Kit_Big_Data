import os
import streamlit as st
import pandas as pd
import logging
from logging_config import setup_logging
from utils.load_csv import initialize_recipes_df

# Initialiser le logger
setup_logging()  # Configuration
logger = logging.getLogger(os.path.basename(__file__))


def load_css(file_name):
    """
    Charge et applique un fichier CSS dans une application Streamlit.
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


# Charger les styles CSS
load_css("style.css")

# Initialiser les donnees dans l'etat de session
initialize_recipes_df("recipes_df", "../data/cloud_df.csv")

# Configuration de l'application Streamlit
st.title("Mange ta main")

st.markdown(
    "Page d'intro expliquant le projet et le but de l'application i.e. son fil rouge "
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
