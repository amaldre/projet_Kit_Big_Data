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
    st.session_state["recipes_df"] = initialize_recipes_df("data/clean_cloud_df.csv")

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
        # Creation of all the graphs displayed in the page
        if st.session_state["first_load"]:
            print(st.session_state["recipes_df"].head())
            trend = compute_trend(st.session_state["recipes_df"])
            logger.info("Tendance calculee avec succes.")

            nb_recette_par_annee_study = BivariateStudy(
                dataframe=trend,
                key="Moyenne glissante du nombre de recettes au cours du temps",
                name="Moyenne glissante du nombre de recettes du temps",
                axis_x="Date",
                axis_y="Moyenne glissante",
                plot_type="plot",
                default_values={
                    "Date": (
                        Timestamp("1999-08-01 00:00:00"),
                        Timestamp("2018-12-1 00:00:00"),
                    ),
                    "Moyenne glissante": (3, 2268),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"] = nb_recette_par_annee_study

            nb_recette_temps_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes en fonction du temps",
                name="Nombre de recettes en fonction du temps",
                axis_x="Date de publication de la recette",
                filters=[],
                plot_type="histogram",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Date de publication de la recette": (
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
                axis_x="Date de publication de la recette",
                axis_y="Nombre de commentaires",
                filters=[],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=True,
                default_values={
                    "Date de publication de la recette": (
                        Timestamp("1999-08-06 00:00:00"),
                        Timestamp("2018-12-04 00:00:00"),
                    ),
                    "Nombre de commentaires": (1, 1613),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"] = nb_commentaire_par_annee_study

            nb_recette_temps_active_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes durant le pic d'activité du site",
                name="Nombre de recettes durant le pic d'activité du site",
                axis_x="Date de publication de la recette", 
                filters=[],
                plot_type="histogram", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "Date de publication de la recette": 
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
                axis_x="Nombre de commentaires",
                filters=["Date de publication de la recette"],
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Nombre de commentaires": (0, 1613), 
                    "Date de publication de la recette":
                    (Timestamp('2001-10-01 00:00:00'),
                     Timestamp('2010-10-01 00:00:00')),
                     "chosen_filters":['Date de publication de la recette']
                     },
                )
            st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"] = comment_box_blot

            mean_rating_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution de la note moyenne des recettes",
                name="Distribution de la note moyenne des recettes",
                axis_x="Note moyenne", 
                filters=['Date de publication de la recette'], 
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Note moyenne": (0, 5), 
                    "Date de publication de la recette":
                    (Timestamp('2001-10-01 00:00:00'), 
                     Timestamp('2010-10-01 00:00:00')), 
                     "chosen_filters":['Date de publication de la recette']
                     },
                )
            st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"] = mean_rating_box_blot

            min_popular_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Duree recettes populaires",
                name="Duree recettes populaires",
                axis_x="Durée de la recette (minutes)",
                axis_y="Nombre de commentaires",
                filters=["Note moyenne"],
                plot_type="scatter",
                default_values={
                    "Durée de la recette (minutes)": (1, 279),
                    "Nombre de commentaires": (100, 1613),
                    "Note moyenne": (4, 5),
                    "chosen_filters": ["Note moyenne"],
                },
            )
            st.session_state["locked_graphs"]["Duree recettes populaires"] = min_popular_recipes

            nb_steps_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'étapes des recettes populaires",
                name="Nombre d'étapes des recettes populaires",
                axis_x="Durée de la recette (minutes)",
                axis_y="Nombre de commentaires", filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=True,
                log_axis_y=True,
                default_values={
                    "Durée de la recette (minutes)": (1, 18720),
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(0, 5),
                    "chosen_filters":['Note moyenne']
                    }
                )
            st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"] = nb_steps_recipes

            nb_ing_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'ingrédients des recettes populaires",
                name="Nombre d'ingrédients des recettes populaires",
                axis_x="Nombre d'ingrédients", 
                axis_y="Nombre de commentaires", 
                filters=['Note moyenne'], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "Nombre d'ingrédients": (4, 20), 
                    "Nombre de commentaires": (5, 1613), 
                    "Note moyenne":(4, 5), 
                    "chosen_filters":['Note moyenne'],
                    },
                )
            st.session_state["locked_graphs"]["Nombre d'ingrédients des recettes populaires"] = nb_ing_recipes

            popular_ing = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Ingrédients les plus populaires",
                name="Ingrédients les plus populaires",
                axis_x="Ingrédients",
                filters=['Note moyenne'],
                plot_type="bar_ingredients",
                log_axis_x=False, log_axis_y=False,
                default_values={
                    "Ingrédients": 10,
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                    },
            )
            st.session_state["locked_graphs"]["Ingrédients les plus populaires"] = popular_ing

            calories_recipes = BivariateStudy(
                key="Calories des recettes populaires",
                dataframe=st.session_state["recipes_df"],
                name="Calories des recettes populaires",
                axis_x="Calories",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'], plot_type="density map",
                log_axis_x=True, log_axis_y=True,
                default_values={
                    "Calories": (1, 19383),
                    "Nombre de commentaires": (5, 1613), 
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                    },
                )
            st.session_state["locked_graphs"]["Calories des recettes populaires"] = calories_recipes

            popular_techniques = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Techniques de cuisine les plus populaires",
                name="Techniques de cuisine les plus populaires",
                axis_x="Techniques utilisées",
                filters=['Note moyenne'],
                plot_type="bar_techniques",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Techniques utilisées": 10,
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                    },
            )
            st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"] = popular_techniques

            st.session_state["first_load"] = False
            logger.info("Graphiques initialises avec succes.")

            


        # Page layout 
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
        - La majorité des recettes populaires sont des recettes courtes, avec une durée de préparation inférieure à 100 Durée de la recette (minutes).
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

        st.session_state["locked_graphs"]["Calories des recettes populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Calories des recettes populaires"].name}")
        
        st.session_state["locked_graphs"]["Ingrédients les plus populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Ingrédients les plus populaires"].name}")

        st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"].name}")
        
        
    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
