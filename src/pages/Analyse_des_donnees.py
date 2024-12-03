import os
import logging
import streamlit as st
from utils.classes import bivariateStudy
from pandas import Timestamp
from utils.load_csv import compute_trend, load_df

logger = logging.getLogger(os.path.basename(__file__))

def load_css(file_name):
    """Charge le fichier CSS pour la mise en page Streamlit."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            logger.info(f"CSS chargé depuis {file_name}.")
    except FileNotFoundError as e:
        logger.error(f"Le fichier CSS {file_name} est introuvable : {e}")
        st.error("Le fichier de style CSS est introuvable.")
    except Exception as e:
        logger.exception(f"Erreur lors du chargement du CSS : {e}")
        st.error("Une erreur est survenue lors du chargement du style.")

def load_data():
    """Charge les données dans la session Streamlit."""
    try:
        if "recipes_df" not in st.session_state:
            st.session_state["recipes_df"] = load_df("data/cloud_df.csv")
            logger.info("Données chargées avec succès dans la session Streamlit.")
    except FileNotFoundError as e:
        logger.error(f"Le fichier de données est introuvable : {e}")
        st.error("Le fichier de données est introuvable.")
    except Exception as e:
        logger.exception(f"Erreur lors du chargement des données : {e}")
        st.error("Une erreur est survenue lors du chargement des données.")

def main():
    """Fonction principale de l'application Streamlit."""
    st.title("Analyse des data")
    load_css("style.css")
    load_data()

    if "first_load" not in st.session_state:
        st.session_state["first_load"] = True

    if "locked_graphs" not in st.session_state:
        st.session_state["locked_graphs"] = []

    try:
        if st.session_state["first_load"]:
            trend = compute_trend(st.session_state["recipes_df"])
            logger.info("Tendance calculée avec succès.")

            nb_recette_par_annee_study = bivariateStudy(
                dataframe=trend,
                key="1",
                name="Moyenne du nombre de recettes au cours du temps",
                axis_x="Date",
                axis_y="Trend",
                plot_type="plot",
                default_values={
                    "Date": (Timestamp('1999-08-01 00:00:00'), Timestamp('2018-12-1 00:00:00')),
                    "Trend": (3, 2268),
                    "chosen_filters": []
                }
            )
            st.session_state["locked_graphs"].append(nb_recette_par_annee_study)

            min_popular_recipes = bivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="2",
                name="Durée recettes populaires",
                axis_x="minutes",
                axis_y="comment_count",
                filters=['mean_rating'],
                plot_type="scatter",
                default_values={
                    "minutes": (1, 279),
                    "comment_count": (100, 1613),
                    "mean_rating": (4, 5),
                    "chosen_filters": ['mean_rating']
                }
            )
            st.session_state["locked_graphs"].append(min_popular_recipes)

            st.session_state["first_load"] = False
            logger.info("Graphiques initialisés avec succès.")
        
        for graph in st.session_state["locked_graphs"]:
            graph.display_graph()
            logger.info(f"Graphique affiché : {graph.name}")

    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'exécution de l'application.")

if __name__ == "__main__":
    main()
