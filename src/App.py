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
load_css("style.css")

# Initialiser les donnees dans l'etat de session
if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("../data/cloud_df.csv")


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
