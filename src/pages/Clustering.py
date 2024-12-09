"""
Cette page présente le Clustering appliqué aux données des recettes.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging
import streamlit.components.v1 as components
import html
from utils.load_functions import load_data, load_css

logger = logging.getLogger(os.path.basename(__file__))

# Paramétrage de Streamlit
st.set_page_config(
    page_title="MangeTaData", page_icon="images/favicon_mangetadata.png", layout="wide"
)


def main():

    PATH_DATA = "data/bertopic_chart/"
    TOPICS_CSV = "topics_model.csv"

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
        À la suite du prétraitement où les données ont été nettoyées, tokenisées et où les stopwords ont été supprimés,
        nous pouvons charger les différentes descriptions et noms des recettes pour les analyser.
        Pour cela, nous récupérons les données du fichier CSV et les transformons en liste de chaînes de caractères.
        Après une analyse et des tests de clustering sur les descriptions, nous préférons finalement utiliser BERTopic 
        sur la colonne *name*, plus représentative des recettes.
        """
    )

    st.header("2️⃣ Réalisation du Clustering avec BERTopic")

    st.write(
        """
        Nous utilisons la librairie BERTopic pour réaliser le Clustering des recettes.
        À l'aide de BERT, un embedding est réalisé pour chaque description de recette.
        Ensuite, nous effectuons le Clustering afin d'identifier les différents types de cuisine.
        Pour cela, BERTopic utilise HDBSCAN. Nous paramétrons ce dernier pour produire des clusters de taille minimale 100.
        De plus, BERTopic utilise UMAP pour la réduction de dimension.
        Nous réduisons ensuite les ~300 topics obtenus à 150 en regroupant les topics les plus proches en dimensions réduites (5).
        """
    )

    st.write(
        """
        Afin d'obtenir les meilleurs résultats possibles et après plusieurs essais,
        nous avons décidé de fournir à BERTopic des 'topic_seeds' avec des mots-clés générés par ChatGPT.
        Ces mots-clés représentent des types de plats ou de cuisines, ce qui permet à BERTopic de mieux identifier les clusters.
        """
    )

    topics_csv = load_data(PATH_DATA, TOPICS_CSV)

    # Afficher les données brutes si elles existent
    if not topics_csv.empty:
        st.write("Exemple des Topics obtenus :")
        st.dataframe(topics_csv.head(10))
    else:
        st.warning("Fichier topics_model.csv introuvable.")
        logger.warning("topics_model.csv introuvable.")

    st.header("3️⃣ Analyse des topics")

    st.write(
        """
        Une visualisation des topics obtenus est disponible ci-dessous.
        Cette représentation 2D permet de visualiser les clusters.
        On remarque que des groupes distincts se forment :
        
        - Dans le coin bas droit, on retrouve les recettes sucrées.
        - Au centre, on retrouve les fruits, les agrumes, certaines épices et sirops.
        - Les recettes salées se retrouvent à l'opposé, dans le coin haut gauche.
        - On observe des recettes de viandes, de poissons, de légumes, d'épices et de nombreux types de sauces.
        - Les recettes de types tartes, quiches, pizzas se regroupent dans le même secteur.
        - De même pour les recettes à base de légumes, qui se retrouvent dans le coin bas gauche.
        """
    )

    st.write(
        """
             Les topics les plus fréquents sont des topcis situé dans les quatres coins de la visualisation. Les recettes populaires peuvent etre sucrées ou salées, des sauces ou des gateaux...
             """
    )

    with open(
        "data/bertopic_chart/visualization_topics.html", "r", encoding="utf-8"
    ) as f:
        html_string = f.read()

    escaped_html = html.escape(html_string)

    iframe_code = f"""
        <iframe srcdoc="{escaped_html}" width="700" height="700" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ffffff;"></iframe>
    """

    st.components.v1.html(iframe_code, height=715, width=715)

    st.header("4️⃣ Visualisation sous forme d'arbres hiérarchiques")

    st.write(
        """
        Voici la visualisation des clusters obtenus avec BERTopic.
        Le pan (outil en haut à droite) permet de se déplacer dans la visualisation.
        """
    )

    with open("data/bertopic_chart/visualization.html", "r", encoding="utf-8") as f:
        html_string = f.read()

    escaped_html = html.escape(html_string)

    iframe_code = f"""
        <iframe srcdoc="{escaped_html}" width="1000" height="800" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ffffff;"></iframe>
    """

    st.components.v1.html(iframe_code, height=820)


if __name__ == "__main__":
    main()
