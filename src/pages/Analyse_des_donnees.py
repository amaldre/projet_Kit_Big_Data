import os
import logging
import streamlit as st
from utils.bivariateStudy import bivariateStudy
from utils.univariateStudy import univariateStudy
from pandas import Timestamp
from utils.load_functions import compute_trend, load_df, initialize_recipes_df, load_css

st.set_page_config(layout="wide")

logger = logging.getLogger(os.path.basename(__file__))


if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("data/cloud_df.csv")

if "first_load" not in st.session_state:
    st.session_state["first_load"] = True

if "locked_graphs" not in st.session_state:
    st.session_state["locked_graphs"] = []


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

            nb_recette_par_annee_study = bivariateStudy(
                dataframe=trend,
                key="1",
                name="Moyenne du nombre de recettes au cours du temps",
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
            st.session_state["locked_graphs"].append(nb_recette_par_annee_study)

            nb_recette_temps_study = univariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="2",
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
            st.session_state["locked_graphs"].append(nb_recette_temps_study)

            nb_commentaire_par_annee_study = bivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="3",
                name="nombre de commentaires par recette en fonction du temps",
                axis_x="submitted", 
                axis_y="comment_count", 
                filters=[], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=True, 
                default_values={
                    "submitted": 
                    (Timestamp('1999-08-06 00:00:00'), 
                     Timestamp('2018-12-04 00:00:00')
                     ), 
                     "comment_count": (1, 1613), 
                     "chosen_filters":[]
                     },
            )
            st.session_state["locked_graphs"].append(nb_recette_temps_study)

            nb_commentaire_par_annee_study = bivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="3",
                name="nombre de commentaires par recette en fonction du temps",
                axis_x="submitted", 
                axis_y="comment_count", 
                filters=[], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=True, 
                default_values={
                    "submitted": 
                    (Timestamp('1999-08-06 00:00:00'), 
                     Timestamp('2018-12-04 00:00:00')), 
                     "comment_count": (1, 1613), 
                     "chosen_filters":[]
                     },
                )
            st.session_state["locked_graphs"].append(nb_commentaire_par_annee_study)

            min_popular_recipes = bivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="4",
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
            st.session_state["locked_graphs"].append(min_popular_recipes)

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
        st.session_state["locked_graphs"][0].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"][0].name}")

        st.session_state["locked_graphs"][1].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"][1].name}")

        st.session_state["locked_graphs"][2].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"][2].name}")


        st.header("2️⃣ Définition d'une recette de populaire")

        st.header("3️⃣ Caractéristiques des recettes populaires")

        explanation_graph_2 = """
        **Observations :**
        - La majorité des recettes populaires sont des recettes courtes, avec une durée de préparation inférieure à 100 minutes.
        - Les recettes populaires ont tendance à avoir un nombre de commentaires plus élevé, avec une concentration autour de 1000 commentaires.

        **Interprétation :**
        - Les recettes courtes pourraient être **plus populaires** car elles sont **plus faciles et rapides à réaliser**.
        - Les recettes populaires génèrent plus de commentaires, ce qui peut indiquer un **engagement plus fort de la part des utilisateurs**.
        """

        st.session_state["locked_graphs"][3].display_graph(
            explanation=explanation_graph_2
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"][3].name}")

    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
