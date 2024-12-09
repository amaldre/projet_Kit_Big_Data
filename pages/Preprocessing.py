"""
Page expliquant les étapes de prétraitement des données.
"""

import streamlit as st
import pandas as pd
import os
import logging
from src.utils.load_functions import load_data, load_css
import html

logger = logging.getLogger(os.path.basename(__file__))

# Variables globales pour simuler les données
PATH_DATA = "data/"
RAW_RECIPE = "RAW_recipes_sample.csv"
RAW_INTERACTIONS = "RAW_interactions_sample.csv"
DF_FINAL = "clean_cloud_df.csv"

try:
    st.set_page_config(
        page_title="MangeTaData",
        page_icon="images/favicon_mangetadata.png",
        layout="wide",
    )
except Exception as e:
    logger.error(f"Erreur lors de la configuration de la page : {e}")
    st.error("Une erreur s'est produite lors de la configuration de la page.")

load_css("src/style.css")


def main():
    st.title("🌟 Explication du Prétraitement des Données")
    st.write(
        """
    Cette page présente les étapes de prétraitement appliquées aux données, 
    ainsi que des visualisations pour mieux comprendre leur impact.
    """
    )
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

    # Afficher les données brutes
    if not raw_recipes.empty:
        st.write("Exemple de données brutes de RAW_recipes :")
        st.dataframe(raw_recipes.head(5))
    else:
        st.warning("Fichier RAW_recipes_sample.csv introuvable.")
        logger.warning("RAW_recipes_sample.csv introuvable.")

    if not raw_interactions.empty:
        st.write("Exemple de données brutes de RAW_interactions :")
        st.dataframe(raw_interactions.head(5))
    else:
        st.warning("Fichier RAW_interactions_sample.csv introuvable.")
        logger.warning("RAW_interactions_sample.csv introuvable.")

    with open("data/Food_data_drawio.html", "r", encoding="utf-8") as f:
        html_string = f.read()

    escaped_html = html.escape(html_string)

    st.write("Drawio de la base de données brutes, données de Kaggle :")
    iframe_code = f"""
        <iframe srcdoc="{escaped_html}" width="1000" height="800" style="border: 2px solid #55381f; border-radius: 20px; background-color: #ffffff;"></iframe>
    """

    st.components.v1.html(iframe_code, height=820)

    st.header("Transformation des Données")
    st.write(
        """
    Plusieurs transformations sont appliquées pour préparer les données :
    1. Les jeux de données doivent être nettoyés.
       - Les recettes avec des valeurs manquantes sont supprimées.
       - Les recettes avec des valeurs aberrantes sont également supprimées, notamment celles avec un temps de cuisson excessif ou un nombre d’étapes nul.
       - Les descriptions manquantes sont remplies avec le contenu de `name` pour combler les vides.
       
    2. Les données de `RAW_interactions` sont fusionnées avec `RAW_recipes`.
       - Les deux DataFrames sont fusionnés sur la colonne `recipe_id`.
       - Les colonnes d’interactions sont transformées en listes pour faire correspondre chaque recette à ses interactions, ses commentaires, ses reviews, etc.

    3. Fusion des jeux de données `RAW_recipes` et `RAW_interactions`.

    4. Nettoyage des descriptions et des noms.
       - Dans le but de réaliser un clustering, les descriptions et les noms des recettes sont nettoyés et tokenisés.
       - Les stopwords sont supprimés des textes.
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
            logger.error(
                f"Erreur lors de la conversion de la colonne `submitted` : {e}"
            )
            st.error(
                "Erreur lors de la conversion des colonnes. Veuillez vérifier vos données."
            )

    st.header("1️⃣ Nettoyage des Données")
    st.write(
        """
    Les colonnes contenant des valeurs manquantes sont remplacées ou supprimées :
    - La colonne `description` est remplie avec le contenu de `name` si elle est vide.
    - Les lignes avec `name` manquant sont supprimées.
        """
    )
    st.write("Nombre de recettes sans noms avant le prétraitement : *4980*")

    st.header("2️⃣ Préparation à la Fusion des Données")
    st.write(
        """
    Les données de `RAW_interactions` sont fusionnées avec `RAW_recipes` :
    - Les deux jeux de données sont joints sur la colonne `recipe_id`.
    - Les colonnes de `RAW_interactions` sont transformées en listes.
        """
    )

    st.header("3️⃣ Suppression des Valeurs Aberrantes")
    st.write(
        """
    Certaines recettes « troll » ou mal renseignées sont supprimées :
    - Les recettes avec un temps de cuisson excessif.
    - Les recettes avec un nombre d’étapes ou d’ingrédients nul.
    - Après avoir séparé la colonne `nutrition` et n’avoir gardé que l’information sur les calories, les recettes avec un nombre de calories excessif sont supprimées.
    - Dans un souci de taille de la base de données, le vecteur des techniques de cuisson est retransformé en mots.
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

    st.header("4️⃣ Nettoyage et Tokenisation des Textes")
    st.write(
        """
    Les descriptions et noms des recettes sont nettoyés et tokenisés :
    - Suppression des stopwords.
    - Tokenisation des phrases en mots.
        """
    )

    try:
        example_text = (
            "This is a recipe with a lot of unnecessary words and punctuation!!!"
        )
        stopwords = {"this", "is", "a", "and"}
        cleaned_text = " ".join(
            [word for word in example_text.lower().split() if word not in stopwords]
        )
        st.write(f"**Texte brut** : {example_text}")
        st.write(f"**Texte nettoyé** : {cleaned_text}")
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des textes : {e}")
        st.error("Impossible de nettoyer les textes.")

    st.header("5️⃣ Mise en place d'une Base de Données")
    st.write(
        """
    Afin de déployer notre application, une base de données MongoDB a été mise en place.
    Nous avons alors tenté d'utiliser MongoDB Atlas.
    Pour cela, nous avons réduit le nombre de colonnes de notre base en supprimant les colonnes inutiles.
    Nous avons gardé uniquement les colonnes suivantes car la version gratuite de MongoDB Atlas nous limitait à 512 Mo :
        """
    )

    cols = st.columns(4)
    columns = [
        "recipe_id",
        "rating",
        "minutes",
        "ingredients",
        "techniques",
        "calories",
        "n_steps",
        "submitted",
    ]

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="padding:10px; border:1px solid #ddd; border-radius:8px; background-color:#ffffff; margin-bottom:10px;">
                    <strong>{columns[i]}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if i + 4 < len(columns):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="padding:10px; border:1px solid #ddd; border-radius:8px; background-color:#ffffff; margin-bottom:10px;">
                        <strong>{columns[i + 4]}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.write(
        """
    Des fonctions permettent d’ajouter les colonnes correspondant aux moyennes des recettes et au nombre de commentaires.
    
    Après avoir créé notre collection et inséré nos données, nous avons pu nous connecter à notre base via une classe Python dédiée.
    Cependant, la version gratuite de MongoDB Atlas nous a limités dans le téléchargement des données (10 Go sur une période glissante de 7 jours), 
    épuisant rapidement notre quota lors des tests. Nous avons donc abandonné MongoDB Atlas au profit d’une base locale réduite à 120 Mo.
    
    Les colonnes sont alors renommées comme suit :
        """
    )

    cols = st.columns(5)
    columns = [
        "Nom",
        "Note moyenne",
        "Nombre de commentaires",
        "Date de publication de la recette",
        "Durée de la recette (minutes)",
        "Ingrédients",
        "Calories",
        "Techniques utilisées",
        "Nombre d'étapes",
        "Dates des commentaires",
    ]

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div style="padding:10px; border:1px solid #ddd; border-radius:8px; background-color:#ffffff; margin-bottom:10px;">
                    <strong>{columns[i]}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if i + 4 < len(columns):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="padding:10px; border:1px solid #ddd; border-radius:8px; background-color:#ffffff; margin-bottom:10px;">
                        <strong>{columns[i + 4]}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    df_final = load_data(PATH_DATA, DF_FINAL)

    # afficher les données finales
    if not df_final.empty:
        st.write("Le DataFrame final est alors le suivant :")
        st.dataframe(df_final.head(5))
    else:
        st.warning("Fichier cloud_recipe_df.csv introuvable.")
        logger.warning("clean_cloud_df.csv introuvable.")


if __name__ == "__main__":
    main()