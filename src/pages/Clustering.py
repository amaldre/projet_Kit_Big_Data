import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(os.path.basename(__file__))

# Paramétrage de Streamlit
st.set_page_config(page_title="Explication Prétraitement", layout="wide")

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        logger.info(f"Le fichier CSS {file_name} a été chargé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier CSS {file_name}: {e}")
        st.error(f"Une erreur est survenue lors du chargement du fichier CSS. Veuillez vérifier le fichier.")

# Charger le CSS
load_css("style.css")

# Titre et description de la page
st.title("👨‍🍳 Clustering des recettes pour analyser les types de cuisine")
st.write(
    """
Cette page présente le Clustering appliqué aux données de recettes,
afin d'identifier les différents types de cuisine.
"""
)

st.header("1️⃣ Chargement des données")

st.write(
    """
         A la suite du pré traitement ou les données ont été nétoyées, tokenisées et ou les stop words ont été supprimés,
         nous pouvons charger les différentes descriptions des recettes pour les analyser.
         Pour cela nous récupérons les données du fichier csv et nous les transformons en Liste de String.
    """
)

st.header("2️⃣ Réalisation du Clustering avec BERTopic")

st.write(
    """
        Nous utilisons la librairie BERTopic pour réaliser le Clustering des recettes.
        A l'aide de BERT, un embeding est réalisé pour chaque description de recette.
        Ensuite, nous réalisons le Clustering pour identifier les différents types de cuisine.
        Pour cela, BERTopic utilise HDBSCAN. Nous paramètrons ce dernier pour faire des clusters de taille minimum 100. 
        De plus, BERTopic utilise UMAP pour la réduction de dimension.
    """
)

st.write(
    """
        Afin d'obtenir les meilleurs résultats possibles et après plusieurs essais,
        nous avons décidé de fournir à BERTopic une 'topic_seeds' avec des mots clés générés par chatGPT. 
    """
)

def create_scrolling_banner(texte: str):
    try:
        scrolling_banner = (
            """
        <style>
        .scrolling-banner {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: #f0f2f6; /* Couleur de fond du bandeau */
            overflow: hidden;
            height: 50px; /* Hauteur du bandeau */
            z-index: 9999; /* Assure que le bandeau reste au-dessus des autres éléments */
        }

        .scrolling-banner h1 {
            position: absolute;
            width: 100%;
            height: 50px;
            line-height: 50px;
            margin: 0;
            font-size: 24px;
            color: #4CAF50; /* Couleur du texte */
            text-align: center;
            transform: translateX(100%);
            animation: scroll-left 10s linear infinite;
        }

        /* Animation pour le défilement du texte */
        @keyframes scroll-left {
            from {
                transform: translateX(100%);
            }
            to {
                transform: translateX(-100%);
            }
        }
        </style>

        <div class="scrolling-banner">
            <h1>"""
            + texte
            + """</h1>
        </div>
        """
        )
        logger.info("Bannière défilante créée avec succès.")
        return scrolling_banner
    except Exception as e:
        logger.error(f"Erreur lors de la création de la bannière défilante: {e}")
        st.error("Une erreur est survenue lors de la création de la bannière défilante.")

# Affichage de la bannière défilante
scrolling_banner = create_scrolling_banner("Texte à faire défiler")
st.components.v1.html(scrolling_banner, height=60)

