"""
Page de l'application dédiée à l'analyse des données.
"""

import os
import logging
import streamlit as st
from utils.bivariate_study import BivariateStudy
from utils.univariate_study import UnivariateStudy
from pandas import Timestamp
from utils.load_functions import compute_trend, load_df, initialize_recipes_df, load_css

st.set_page_config(layout="wide")

logger = logging.getLogger(os.path.basename(__file__))


if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("data/cloud_df.csv")

if "first_load" not in st.session_state:
    st.session_state["first_load"] = True

if "locked_graphs" not in st.session_state:
    st.session_state["locked_graphs"] = {}


def main():
    """
    Fonction principale de la page Analyse des données.
    """
    st.title("Analyse des data")
    load_css("src/style.css")

    try:
        if st.session_state["first_load"]:
            trend = compute_trend(st.session_state["recipes_df"])
            logger.info("Tendance calculee avec succes.")

            nb_recette_par_annee_study = BivariateStudy(
                dataframe=trend,
                key="Moyenne glissante du nombre de recettes au cours du temps",
                name="Moyenne glissante du nombre de recettes du temps",
                axis_x="Date",
                axis_y="Trend",
                plot_type="plot",
                default_values={
                    "Date": (
                        Timestamp("1999-08-01 00:00:00"),
                        Timestamp("2018-12-1 00:00:00"),
                    ),
                    "Trend": (3, 2268),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"] = nb_recette_par_annee_study

            nb_recette_temps_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes en fonction du temps",
                name="Nombre de recettes en fonction du temps",
                axis_x="submitted",
                filters=[],
                plot_type="histogram",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "submitted": (
                        Timestamp("1999-08-06 00:00:00"),
                        Timestamp("2018-12-04 00:00:00"),
                    ),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Nombre de recettes en fonction du temps"] = nb_recette_temps_study

            

            nb_commentaire_par_annee_study = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de commentaires par recette en fonction du temps",
                name="Nombre de commentaires par recette en fonction du temps",
                axis_x="submitted",
                axis_y="comment_count",
                filters=[],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=True,
                default_values={
                    "submitted": (
                        Timestamp("1999-08-06 00:00:00"),
                        Timestamp("2018-12-04 00:00:00"),
                    ),
                    "comment_count": (1, 1613),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"] = nb_commentaire_par_annee_study

            nb_recette_temps_active_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes durant le pic d'activité du site",
                name="Nombre de recettes durant le pic d'activité du site",
                axis_x="submitted", 
                filters=[],
                plot_type="histogram", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "submitted": 
                    (Timestamp('2001-10-01 00:00:00'), 
                     Timestamp('2010-10-01 00:00:00')), 
                     "chosen_filters":[]
                     },
            )
            st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"] = nb_recette_temps_active_study

            comment_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution du nombre de commentaires par recette",
                name="Distribution du nombre de commentaires par recette",
                axis_x="comment_count",
                filters=["submitted"],
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "comment_count": (0, 1613), 
                    "submitted":
                    (Timestamp('2001-10-01 00:00:00'),
                     Timestamp('2010-10-01 00:00:00')),
                     "chosen_filters":['submitted']
                     },
                )
            st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"] = comment_box_blot

            mean_rating_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution de la note moyenne des recettes",
                name="Distribution de la note moyenne des recettes",
                axis_x="mean_rating", 
                filters=['submitted'], 
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "mean_rating": (0, 5), 
                    "submitted":
                    (Timestamp('2001-10-01 00:00:00'), 
                     Timestamp('2010-10-01 00:00:00')), 
                     "chosen_filters":['submitted']
                     },
                )
            st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"] = mean_rating_box_blot

            min_popular_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Duree recettes populaires",
                name="Duree recettes populaires",
                axis_x="minutes",
                axis_y="comment_count",
                filters=["mean_rating"],
                plot_type="scatter",
                default_values={
                    "minutes": (1, 279),
                    "comment_count": (100, 1613),
                    "mean_rating": (4, 5),
                    "chosen_filters": ["mean_rating"],
                },
            )
            st.session_state["locked_graphs"]["Duree recettes populaires"] = min_popular_recipes

            nb_steps_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'étapes des recettes populaires",
                name="Nombre d'étapes des recettes populaires",
                axis_x="n_steps", 
                axis_y="comment_count", 
                filters=['mean_rating'], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "n_steps": (3, 37), 
                    "comment_count": (5, 1613), 
                    "mean_rating":(4, 5), 
                    "chosen_filters":['mean_rating'],
                    },
                )
            st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"] = nb_steps_recipes

            nb_ing_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'ingrédients des recettes populaires",
                name="Nombre d'ingrédients des recettes populaires",
                axis_x="ingredient_count", 
                axis_y="comment_count", 
                filters=['mean_rating'], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "ingredient_count": (4, 20), 
                    "comment_count": (5, 1613), 
                    "mean_rating":(4, 5), 
                    "chosen_filters":['mean_rating'],
                    },
                )
            st.session_state["locked_graphs"]["Nombre d'ingrédients des recettes populaires"] = nb_ing_recipes

            st.session_state["first_load"] = False
            logger.info("Graphiques initialises avec succes.")

        st.header("1️⃣ Analyse de la fréquentation du site")

        explanation_graph_1 = """
        **Observations :**
        - Une forte croissance des contributions est visible entre 2000 et 2008, culminant à une activité maximale autour de 2008.
        - À partir de 2008, une chute significative et prolongée est observée, atteignant presque zéro vers 2016-2018.

        **Interprétation :**
        - Cette baisse reflète une **diminution marquée de l'activité des utilisateurs créateurs de contenu**, probablement due à plusieurs facteurs :
          1. **Concurrence croissante** : Avec l'émergence de plateformes sociales comme YouTube, Instagram, et des sites concurrents, le site aurait pu perdre son attractivité.
          2. **Fatigue des contributeurs** : Les créateurs pourraient avoir perdu intérêt ou ne pas être suffisamment motivés pour continuer à enrichir la plateforme.
          3. **Manque d'innovation** : Si le site n'a pas évolué pour répondre aux nouvelles attentes des utilisateurs (fonctionnalités modernes, gamification, etc.), il aurait pu perdre de l'engagement.
        """
        st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].name}")

        st.session_state["locked_graphs"]["Nombre de recettes en fonction du temps"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes en fonction du temps"].name}")

        st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].name}")

        st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].name}")

        st.header("2️⃣ Définition d'une recette de populaire")

        st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].name}")

        st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].name}")

        

        st.header("3️⃣ Caractéristiques des recettes populaires")
        

        explanation_graph_2 = """
        **Observations :**
        - La majorité des recettes populaires sont des recettes courtes, avec une durée de préparation inférieure à 100 minutes.
        - Les recettes populaires ont tendance à avoir un nombre de commentaires plus élevé, avec une concentration autour de 1000 commentaires.

        **Interprétation :**
        - Les recettes courtes pourraient être **plus populaires** car elles sont **plus faciles et rapides à réaliser**.
        - Les recettes populaires génèrent plus de commentaires, ce qui peut indiquer un **engagement plus fort de la part des utilisateurs**.
        """

        st.session_state["locked_graphs"]["Duree recettes populaires"].display_graph(
            explanation=explanation_graph_2
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Duree recettes populaires"].name}")

        st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].name}")

        st.session_state["locked_graphs"]["Nombre d'ingrédients des recettes populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'ingrédients des recettes populaires"].name}")
        

    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
