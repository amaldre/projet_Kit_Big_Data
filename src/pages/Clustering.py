import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Explication Prétraitement", layout="wide")

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
        Pour cela, BERTopic utilise HDBSCAN. Nous paramètrés ce dernier pour faire des cluster de taille minimum 100. 
        De plus BERTopic utilise UMAP pour la réduction de dimension.
    """
)

st.write(
    """
        Afin d'obtenir les meilleurs résultats possibles et après plusieurs essaies,
        nous avons décidé de fournir à BERTopic une 'topic_seeds' avec des mots clés généré par chatGPT. 
        """
)


scrolling_banner = """
<style>
/* Styles pour le bandeau défilant */
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
    <h1>Bienvenue sur mon application Streamlit ! Profitez de nos dernières mises à jour.</h1>
</div>
"""

st.components.v1.html(scrolling_banner, height=60)
