import os
import logging
import streamlit as st
from utils.classes import bivariateStudy
from pandas import Timestamp
from utils.load_csv import compute_trend, load_df, initialize_recipes_df

logger = logging.getLogger(os.path.basename(__file__))


def load_css(file_name):
    """Charge le fichier CSS pour la mise en page Streamlit."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            logger.info(f"CSS charge depuis {file_name}.")
    except FileNotFoundError as e:
        logger.error(f"Le fichier CSS {file_name} est introuvable : {e}")
        st.error("Le fichier de style CSS est introuvable.")
    except Exception as e:
        logger.exception(f"Erreur lors du chargement du CSS : {e}")
        st.error("Une erreur est survenue lors du chargement du style.")


def afficher_texte(graph):
    """Affiche un texte dans l'application Streamlit."""
    if graph.name == "Moyenne du nombre de recettes au cours du temps":
        st.write(
            """
        **Observations :**
        - Une forte croissance des contributions est visible entre 2000 et 2008, culminant à une activité maximale autour de 2008.
        - À partir de 2008, une chute significative et prolongée est observée, atteignant presque zéro vers 2016-2018.

        **Interprétation :**
        - Cette baisse reflète une **diminution marquée de l'activité des utilisateurs créateurs de contenu**, probablement due à plusieurs facteurs :
          1. **Concurrence croissante** : Avec l'émergence de plateformes sociales comme YouTube, Instagram, et des sites concurrents, le site aurait pu perdre son attractivité.
          2. **Fatigue des contributeurs** : Les créateurs pourraient avoir perdu intérêt ou ne pas être suffisamment motivés pour continuer à enrichir la plateforme.
          3. **Manque d'innovation** : Si le site n'a pas évolué pour répondre aux nouvelles attentes des utilisateurs (fonctionnalités modernes, gamification, etc.), il aurait pu perdre de l'engagement.
        """
        )
    elif graph.name == "Duree recettes populaires":
        st.write(
            """
        **Observations :**
        - La majorité des recettes populaires sont des recettes courtes, avec une durée de préparation inférieure à 100 minutes.
        - Les recettes populaires ont tendance à avoir un nombre de commentaires plus élevé, avec une concentration autour de 1000 commentaires.

        **Interprétation :**
        - Les recettes courtes pourraient être **plus populaires** car elles sont **plus faciles et rapides à réaliser**.
        - Les recettes populaires génèrent plus de commentaires, ce qui peut indiquer un **engagement plus fort de la part des utilisateurs**.
        """
        )


def main():
    """Fonction principale de l'application Streamlit."""
    st.title("Analyse des data")
    load_css("style.css")
    initialize_recipes_df("recipes_df", "../../data/cloud_df.csv")

    if "first_load" not in st.session_state:
        st.session_state["first_load"] = True

    if "locked_graphs" not in st.session_state:
        st.session_state["locked_graphs"] = []

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

            min_popular_recipes = bivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="2",
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

        for graph in st.session_state["locked_graphs"]:
            graph.display_graph()
            afficher_texte(graph)
            logger.info(f"Graphique affiche : {graph.name}")

    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
