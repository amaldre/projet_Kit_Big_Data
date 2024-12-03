import os
import streamlit as st
import pandas as pd
import logging
from logging_config import setup_logging
from utils.load_csv import load_df

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
            logger.info(f"CSS chargé avec succès depuis '{file_name}'.")
    except FileNotFoundError:
        error_message = f"Le fichier CSS '{file_name}' est introuvable."
        logger.error(error_message)
        st.error(error_message)
    except Exception as e:
        error_message = f"Une erreur inattendue s'est produite lors du chargement du CSS : {e}"
        logger.exception(error_message)
        st.error(error_message)

def initialize_recipes_df(session_key, file_path):
    """
    Initialise le DataFrame dans l'état de session de Streamlit.
    """
    if session_key not in st.session_state:
        try:
            st.session_state[session_key] = load_df(file_path)
            logger.info(f"DataFrame chargé avec succès depuis '{file_path}'.")
        except FileNotFoundError:
            error_message = f"Le fichier CSV '{file_path}' est introuvable."
            logger.error(error_message)
            st.error(error_message)
            st.session_state[session_key] = pd.DataFrame()  # Charger un DataFrame vide en cas d'erreur
        except pd.errors.ParserError:
            error_message = "Erreur lors du traitement du fichier CSV. Veuillez vérifier son format."
            logger.error(error_message)
            st.error(error_message)
            st.session_state[session_key] = pd.DataFrame()
        except Exception as e:
            error_message = f"Une erreur inattendue s'est produite lors du chargement du CSV : {e}"
            logger.exception(error_message)
            st.error(error_message)
            st.session_state[session_key] = pd.DataFrame()

# Charger les styles CSS
load_css("style.css")

# Initialiser les données dans l'état de session
initialize_recipes_df("recipes_df", "../data/cloud_df.csv")

# Configuration de l'application Streamlit
st.title("Mange ta main")

st.markdown(
    "Page d'intro expliquant le projet et le but de l'application i.e. son fil rouge "
)
