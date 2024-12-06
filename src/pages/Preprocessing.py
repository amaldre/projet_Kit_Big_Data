import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import ast
import nltk
import re
from utils.dbapi import DBapi
import logging
from utils.load_functions import load_data, load_css
import html


logger = logging.getLogger(os.path.basename(__file__))

# db = DBapi()
# with db:
#     df = pd.DataFrame(db.get_percentage_documents(per=0.0005))

# Variables globales pour simuler les données
PATH_DATA = "data/"
RAW_RECIPE = "RAW_recipes_sample.csv"
RAW_INTERACTIONS = "RAW_interactions_sample.csv"

# ---- Page Streamlit ----
try:
    st.set_page_config(page_title="Explication Prétraitement", layout="wide")
except Exception as e:
    logger.error(f"Erreur lors de la configuration de la page : {e}")
    st.error("Une erreur s'est produite lors de la configuration de la page.")


load_css("src/style.css")

# --- Titre et Introduction ---
st.title("🌟 Explication du Prétraitement des Données")
st.write(
    """
Cette page présente les étapes de prétraitement appliquées aux données, 
ainsi que des visualisations pour mieux comprendre leur impact.
"""
)

# --- Chargement des données ---
st.header("Chargement des Données")
st.write(
    """
Les données brutes sont chargées à partir de fichiers CSV. Voici un aperçu des fichiers utilisés :
- `RAW_recipes.csv` : Données des recettes brutes.
- `RAW_interactions.csv` : Interactions des utilisateurs avec les recettes.
"""
)


raw_recipes = load_data(PATH_DATA, RAW_RECIPE)
raw_interactions = load_data(PATH_DATA, RAW_INTERACTIONS)

# Afficher les données brutes si elles existent
if not raw_recipes.empty:
    st.write("Exemple de données brutes de RAW_recipe:")
    st.dataframe(raw_recipes.head(5))
else:
    st.warning("Fichier RAW_recipes_sample.csv introuvable.")
    logger.warning("RAW_recipes_sample.csv introuvable.")

if not raw_interactions.empty:
    st.write("Exemple de données brutes de RAW_interactions:")
    st.dataframe(raw_interactions.head(5))
else:
    st.warning("Fichier RAW_interactions_sample.csv introuvable.")
    logger.warning("RAW_interactions_sample.csv introuvable.")

with open("data/Food_data_drawio.html", "r", encoding="utf-8") as f:
    html_string = f.read()

# Échapper les guillemets du contenu HTML

escaped_html = html.escape(html_string)

# Créer le code HTML de l'iframe avec des styles pour les bords arrondis
iframe_code = f"""
    <iframe srcdoc="{escaped_html}" width="1000" height="800" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ebcdac;"></iframe>
"""

st.components.v1.html(iframe_code, height=820)


# --- Transformation des Données ---
st.header(" Transformation des Données")
st.write(
    """
Plusieurs transformations sont appliquées pour préparer les données :
1. Les datasets doivent être nettoyés.
    Pour cela, les recettes avec des valeurs manquantes sont supprimées.
    Les recettes avec des valeurs aberrantes sont également supprimées.
    Notamment celles avec un temps de cuisson excessif ou un nombre de steps nul.
    Les 'Description' manquantes sont remplies avec le contenu de 'Name' pour combler les vides.
    
2. Les données de RAW_interactions devaient être fusionnées avec RAW_recipes. Pour cela, les deux dataframes ont été merge sur la colonne `recipe_id`.
Les colonnes de interactions ont été transformées en listes pour faire correspondre chaque recette avec ses interactions, ses commentaires, ses reviews, etc.

3. Fusion des datasets `RAW_recipes` et `RAW_interactions`.

4. Nettoyage des descriptions et des noms.
   Dans le but de réaliser un clustering, les descriptions et les noms des recettes sont nettoyés et tokenisés.
   Les stopwords sont supprimés des textes.

"""
)

# Exemple visuel avant/après nettoyage
if not raw_recipes.empty:
    try:
        raw_recipes["submitted"] = pd.to_datetime(
            raw_recipes.get("submitted", pd.Series([])), errors="coerce"
        )
        st.write(
            "**Avant conversion de la colonne `submitted` :**",
            raw_recipes["tags"].dtype,
        )
        st.write("**Après conversion :**", raw_recipes["tags"].dtype)
    except Exception as e:
        logger.error(f"Erreur lors de la conversion de la colonne `submitted` : {e}")
        st.error(
            "Erreur lors de la conversion des colonnes. Veuillez vérifier vos données."
        )

# --- Nettoyage des Données ---
st.header("1️⃣ Nettoyage des Données")
st.write(
    """
Les colonnes contenant des valeurs manquantes sont remplacées ou supprimées :
- La colonne `description` est remplie avec le contenu de `name` si elle est vide.
- Les lignes avec `name` manquant sont supprimées.
"""
)

# Visualisation des valeurs manquantes
if not raw_recipes.empty:
    try:
        st.write("Visualisation des valeurs manquantes dans les données brutes :")
        missing_data = raw_recipes.isna().sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(missing_data.index, missing_data.values)
        ax.set_title("Valeurs manquantes par colonne")
        ax.set_xlabel("Nombre de valeurs manquantes")
        st.pyplot(fig)
    except Exception as e:
        logger.error(f"Erreur lors de la visualisation des valeurs manquantes : {e}")
        st.error("Impossible de visualiser les valeurs manquantes.")

# --- Préparation à la fusion des Données ---
st.header("2️⃣ Préparation à la fusion des Données")
st.write(
    """
Les données de RAW_interactions sont fusionnées avec RAW_recipes :
- Les deux datasets sont joints sur la colonne recipe_id.
- Les colonnes de RAW_interactions sont transformées en listes.
"""
)

# --- Visualisation de la Fusion ---
st.header("3️⃣ Visualisation de la Fusion")

# --- Suppression des Valeurs Aberrantes ---
st.header("4️⃣ Suppression des Valeurs Aberrantes")
st.write(
    """
Certaines recettes troll ou mal renseignées sont supprimées :
- Les recettes avec un temps de cuisson excessif.
- Les recettes avec un nombre de steps ou d'ingrédients nul.
"""
)

# Exemple fictif
if not raw_recipes.empty:
    try:
        cleaned_recipes = raw_recipes[raw_recipes["minutes"] < 300]
        st.write(f"Recettes avant nettoyage : {len(raw_recipes)}")
        st.write(f"Recettes après nettoyage : {len(cleaned_recipes)}")
    except KeyError as e:
        logger.error(f"Erreur : Colonne manquante dans le DataFrame : {e}")
        st.error(
            "Certaines colonnes nécessaires pour le nettoyage des données sont manquantes."
        )
    except Exception as e:
        logger.error(f"Erreur lors de la suppression des valeurs aberrantes : {e}")
        st.error("Une erreur est survenue lors du nettoyage des données.")

# --- Nettoyage des Textes ---
st.header("5️⃣ Nettoyage et Tokenisation des Textes")
st.write(
    """
Les descriptions et noms des recettes sont nettoyés et tokenisés :
- Suppression des stopwords.
- Tokenisation des phrases en mots.
"""
)

try:
    example_text = "This is a recipe with a lot of unnecessary words and punctuation!!!"
    stopwords = {"this", "is", "a", "and"}
    cleaned_text = " ".join(
        [word for word in example_text.lower().split() if word not in stopwords]
    )
    st.write(f"**Texte brut** : {example_text}")
    st.write(f"**Texte nettoyé** : {cleaned_text}")
except Exception as e:
    logger.error(f"Erreur lors du nettoyage des textes : {e}")
    st.error("Impossible de nettoyer les textes.")

# --- Pipeline de Prétraitement ---
st.header("6️⃣ Visualisation du Pipeline")
from graphviz import Digraph

try:
    dot = Digraph()
    dot.node("A", "Chargement")
    dot.node("B", "Fusion")
    dot.node("C", "Nettoyage")
    dot.node("D", "Suppression des Outliers")
    dot.node("E", "Tokenisation")
    dot.edges(["AB", "BC", "CD", "DE"])
    st.graphviz_chart(dot)
except Exception as e:
    logger.error(f"Erreur lors de la creation du pipeline visuel : {e}")
    st.error("Impossible de visualiser le pipeline.")

# --- Mise en place d'une base de données ---
st.header("7️⃣ Mise en place d'une base de données")
st.write(
    """
Afin de déployer notre application, nous avons mis en place une base de données MongoDB.
Nous avons alors tenté d'utiliser MongoDB Atlas.
Pour cela nous avons réduit le nombre de colonnes de notre base en supprimant les colonnes inutiles.
Nous avons alors gardé uniquement les colonnes suivantes car la version gratuite de MongoDB Atlas nous limitait à 512 Mo de données :
- recipe_id
- name
- rating
- minutes
- ingredients
- n_steps

Après avoir créé notre collection et inséré nos données, nous avons pu nous connecter à notre base de données via une classe Python créée pour l'occasion.
Cependant, la version gratuite de MongoDB Atlas nous a limité dans le téléchargement de nos données. Le téléchargement étant limité à 10 Go sur une période glissante de 7 jours, nous avons au cours de nos tests épuisé notre quota de téléchargement.
Nous avons donc abandonné l'utilisation de MongoDB Atlas pour une base de données locale réduite à 120 Mo.
"""
)

# TODO : Raconter mieux lhistoire du pretaitement
