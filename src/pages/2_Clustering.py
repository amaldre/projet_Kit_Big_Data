"""
Cette page presente le Clustering appliqué aux donnees des recettes.
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

# Parametrage de Streamlit
st.set_page_config(page_title="Explication Pretraitement", layout="wide")


def main():

    PATH_DATA = "data/bertopic_chart/"
    TOPICS_CSV = "topics_model.csv"

    # Charger le CSS
    load_css("src/style.css")

    # Titre et description de la page
    st.title("👨‍🍳 Clustering des recettes pour analyser les types de cuisine")
    st.write(
        """
    Cette page presente le Clustering applique aux donnees de recettes,
    afin d'identifier les differents types de cuisine.
    """
    )

    st.header("1️⃣ Chargement des donnees")

    st.write(
        """
            A la suite du pre traitement ou les donnees ont ete netoyees, tokenisees et ou les stop words ont ete supprimes,
            nous pouvons charger les differentes descriptions et noms des recettes pour les analyser.
            Pour cela nous recuperons les donnees du fichier csv et nous les transformons en Liste de String.
            Après une analyse et des test de clusterings sur les descriptions, nous preferons finalement utilisé BERTopic sur 
            la colonne *name*, plus representative des recettes. 
        """
    )

    st.header("2️⃣Realisation du Clustering avec BERTopic")

    st.write(
        """
            Nous utilisons la librairie BERTopic pour realiser le Clustering des recettes.
            A l'aide de BERT, un embeding est realise pour chaque description de recette.
            Ensuite, nous realisons le Clustering pour identifier les differents types de cuisine.
            Pour cela, BERTopic utilise HDBSCAN. Nous parametrons ce dernier pour faire des clusters de taille minimum 100. 
            De plus, BERTopic utilise UMAP pour la reduction de dimension.
            Nous reduissons ensuite les ~300 topics obtenus à 150 en regroupant les topics les plus proches en dimension réduites (5)
        """
    )

    st.write(
        """
            Afin d'obtenir les meilleurs resultats possibles et apres plusieurs essais,
            nous avons decide de fournir à BERTopic une 'topic_seeds' avec des mots clés générés par chatGPT.
            Ces mots clés sont des types de plats ou de cuisine qui permettent à BERTopic de mieux identifier les clusters. 
        """
    )

    topics_csv = load_data(PATH_DATA, TOPICS_CSV)

    # Afficher les données brutes si elles existent
    if not topics_csv.empty:
        st.write("Exemple des Topics obtenus:")
        st.dataframe(topics_csv.head(10))
    else:
        st.warning("Fichier topic_model.csv introuvable.")
        logger.warning("topic_model.csv introuvable.")

    st.header("3️⃣ Analyse des topics")

    st.write(
        """
            Une visualisation des topics obtenus est disponible ci-dessous.
            Cette representation 2D permet de visualiser les clusters.
            On remarque que des groupes distincs se forment. 
            
            - Dans le coin bas droit se retrouves les recettes sucrées,
            - Au centre on retrouve les fruits, les agrumes, certaines épices et sirops.
            - Les recettes salées se retrouve à l'opposé, dans le coin haut gauche.
            - On retrouve des recettes de viandes, de poissons, de légumes, d'épices et de nombreux types de sauces. 
            - Les recettes de types tartes, quiches, pizzas se toutes dans le même coin.
            - De même pour les recettes à base de légumes qui se retrouvent dans le coin bas gauche.
            
            """
    )

    with open(
        "data/bertopic_chart/visualization_topics.html", "r", encoding="utf-8"
    ) as f:
        html_string = f.read()

    escaped_html = html.escape(html_string)

    iframe_code = f"""
        <iframe srcdoc="{escaped_html}" width="700" height="700" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ebcdac;"></iframe>
    """

    st.components.v1.html(iframe_code, height=715, width=715)

    st.header("4️⃣ Visualisation sous formes d'arbres hierarchiques")

    st.write(
        """
        Voici la visualisation des clusters obtenus avec BERTopic.
        Le pan (outils en haut à droite) permet de se déplacer dans la visualisation.
        """
    )

    with open("data/bertopic_chart/visualization.html", "r", encoding="utf-8") as f:
        html_string = f.read()

    # Échapper les guillemets du contenu HTML

    escaped_html = html.escape(html_string)

    # Créer le code HTML de l'iframe avec des styles pour les bords arrondis
    iframe_code = f"""
        <iframe srcdoc="{escaped_html}" width="1000" height="800" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ebcdac;"></iframe>
    """

    st.components.v1.html(iframe_code, height=820)


if __name__ == "__main__":
    main()
