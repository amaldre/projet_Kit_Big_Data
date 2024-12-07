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
                key="Moyenne glissante du nombre de recettes par mois",
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
                key="Nombre de recettes par an",
                name="Nombre de recettes par an",
                axis_x="Date de publication de la recette",
                filters=[],
                plot_type="histogram",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Date de publication de la recette": (
                        Timestamp("2000-01-01 00:00:00"),
                        Timestamp("2018-01-01 00:00:00"),
                    ),
                    "chosen_filters": [],
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Nombre de recettes par an"] = nb_recette_temps_study

            

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
                    (Timestamp('2002-01-01 00:00:00'), 
                     Timestamp('2010-01-01 00:00:00')), 
                     "chosen_filters":[]
                },
                graph_pad=1,
                
            )
            st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"] = nb_recette_temps_active_study

            comment_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution du nombre de commentaires par recette",
                name="Distribution du nombre de commentaires par recette",
                axis_x="Nombre de commentaires",
                filters=[],
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Nombre de commentaires": (0, 1613), 
                },
            )
            st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"] = comment_box_blot

            mean_rating_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution de la note moyenne des recettes",
                name="Distribution de la note moyenne des recettes",
                axis_x="Note moyenne", 
                filters=[], 
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Note moyenne": (0, 5), 
                },
            )
            st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"] = mean_rating_box_blot

            min_popular_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Duree recettes populaires",
                name="Duree recettes populaires",
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
                },
            )
            st.session_state["locked_graphs"]["Duree recettes populaires"] = min_popular_recipes

            nb_steps_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'étapes des recettes populaires",
                name="Nombre d'étapes des recettes populaires",
                axis_x="Nombre d'étapes",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Nombre d'étapes": (3, 37),
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
                
            )
            st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"] = nb_steps_recipes

            nb_ing_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'ingrédients par recette",
                name="Nombre d'ingrédients par recette",
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
            st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"] = nb_ing_recipes

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
                dataframe=st.session_state["recipes_df"],
                key="Calories des recettes populaires",
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

            nb_techniques_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de techniques de cuisine différentes par recettes",
                axis_x="Nombre de techniques utilisées",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Nombre de techniques utilisées": (0, 14),
                    "Nombre de commentaires": (1, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
            )
            st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"] = nb_techniques_recipes 

            st.session_state["first_load"] = False
            logger.info("Graphiques initialises avec succes.")

            
        st.write("""Dans cette page, diverses analyses seront effectuées sur les données fournies par le site Food.com, 
                 notamment sur les recettes telles les nombres de recettes publiés, leur note moyenne et nombre commentaires,
                 les ingrédients ou techniques de cuisine utilisés, etc.. 
                 Le but de de cette étude est d'évaluer les performances du site au cours du temps et de comprempre les facteurs de succès 
                 des recettes les plus populaire afin de redynamiser l'activité sur la platforme""")

        # Page layout 
        st.header("1️⃣ Analyse de la fréquentation du site")

        st.write("""Tout d'abord, il s'agira d'étudier la fréquentation du site au cours des années 
                 à travers l'évolution du nombre de recettes ainsi que le nombre de commentaires par recettes.""")

        explanation_graph_1 = """
        **Observations :**
        - Ce graphe représente la moyenne glissante sur par mois du nombre de recettes entre 2000 et 2018
        - Une forte croissance des contributions est visible entre 2000 et 2002, puis une stagnation entre 2002 et 2004 puis une deuxième phase de croissance en 2008, 
        - Le pic d'activité maximale est atteint autour de 2007 et 2008 avec plus de 2000 recettes par mois.
        - À partir de 2008, une chute significative et prolongée est observée, atteignant presque zéro entre 2016 et 2018."""

        
        st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].name}")

        col1, col2 = st.columns(2)
        with col1 :
            st.session_state["locked_graphs"]["Nombre de recettes par an"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes par an"].name}")
        with col2 :
            st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].name}")
        
        with st.container(border=True):
            explanation_graph_2 = """
            **Observations :**
            - Ces deux graphes représentent le nombre de recettes publiés par an sur deux plages d'années différentes. 
            Celui de droite offrant une vue d'ensemble sur toute la période couverte par les données, entre 2000 et 2018 
            Le de gauche se focalise sur la phase de plus grande affluence du site entre 2002 et 2010. 
            - La tendance nombre de publications de recettes précedemment observée est en accord avec ces graphes avec 
            comme année culminante 2007 et 2008 comptant respectivement 26539 et 23238 recettes, puis une chute de l'activité après 2008.
            - De plus, il est intéressant de noter que le pic d'activité représente 151367 recettes sur 176287 au total, soit 
            environ 85% de toutes les recettes publiées.
            """
            st.write(explanation_graph_2)
            

        explanation_graph_3 ="""
        **Observations :**
        - Ce graphe est une carte de densité repésentant l'évolution du nombre de commentaires par recette sur la période étudiée.
        Une forte activité des utilisateurs se traduisant par un nombre de commentaires par recette peut être observée dès 2000 jusqu'à 2009, 
        ce sur une plage temporelle plus étendue comparé au nombre de recettes publiées.
        - Sur cette période un grand nombre de recette dépasse les 20 commentaires et 
        les records de nombre de commentaires sont établis pour les recettes publié dans cet intervalle, 
        atteignant plus de 1600 commentaires pour les meilleurs recettes.
        - De plus, une concentration très important de recettes publiés à ce moment ont entre 1 et 20 commentaires (en jaune et cyan sur le graphe),
        notamment entre 2006 et 2009 qui ont la plus fort concentration recette à 1 commentaires.Cette tendance montre une effervescence de recettes, 
        mais que ces recettes n'attirent pas forcemment beaucoup de personnes, remmettant en cause la qualité des recettes.
        """

        st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].display_graph(
            explanation=explanation_graph_3
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].name}")

        conclusion_part_1 = """
        **Interprétation :**
        - Après une forte croissance jusqu'en 2009, Le site a connu un fort déclin jusqu'à aujoud'hui, qui s'illustre par la diminution marquée de l'activité des utilisateurs
        dans la création de recettes et de l'engagement utilisateurs dans l'espace commentaire.  

        - Cette baisse d'activité peut être expliquer par plusieurs facteurs :
          1. **Concurrence croissante** : Avec l'émergence de plateformes sociales comme YouTube, Instagram, et des sites concurrents, le site aurait pu perdre son attractivité.
          2. **Fatigue des contributeurs** : Les créateurs pourraient avoir perdu intérêt ou ne pas être suffisamment motivés pour continuer à enrichir la plateforme.
          3. **Manque d'innovation** : Si le site n'a pas évolué pour répondre aux nouvelles attentes des utilisateurs (fonctionnalités modernes, gamification, etc.), il aurait pu perdre de l'engagement.
          4. **Facteurs externes** : La crise économique de 2008 a pu engendrée un manque de moyens pour s'investir dans la cuisine maison. 
        
        - La question des solutions de comment remedier à cette tendance et revitaliser le site peut se poser.
          La démarche proposée dans la suite de l'étude est d'analyser en profondeur les recettes les plus populaires ayant portées 
          le site durant son âge d'or, engendrant de l'attractivité et de l'engagement de la part de ses utilisateurs.
        """
        with st.container(border=True):
            st.write(conclusion_part_1)
        

        st.header("2️⃣ Définition d'une recette de populaire")

        st.write("""Dans cette deuxième partie, il conviendra comprendre ce qui définit la popularatié d'une recette
                 Deux axes pricipaux seront explorées : la note moyenne et le nombre de commentaire des recettes""")

        explanation_graph_4 = """
        **Observations :**
        Ce graphe de type boite à moustache illustre la distribution du nombre de commentaires par recette. 
        Plus précisemment, d'après celui-ci, on observe :
        - une médianne situé au alentours de 2 commentaires par recettes
        - 25% des meilleurs recettes en terme de nombre de commentaires ont 5 ou plus de commentaires (Troisième quartile).

        La distribution du nombre de commentaires par recette est très polarisée en faveur des recettes avec peu de commentaires
        avec la grande majorité des recettes ayant en dessous de 5 commentaires, 
        une médiane situé à 2 commentaires et un grand nombre à 1 commentaire (63084 recettes soit 35%).
        Cette analyse confirme le rapport quantité/attractivité à améliorer évoqué dans la première partie.
        """

        st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].display_graph(
            explanation=explanation_graph_4
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].name}")

        explanation_graph_5 = """
        **Observations :**
        Ce graphe de type boite à moustache représente la distribution des notes moyennes des recettes. 
        Plus précisemment, d'après celui-ci, on observe :
        - une médianne située au alentours de la note moyenne de 4,6 commentaires par recette
        - seulement 25% des recettes sont notés 4 ou moins (1er quartile).

        Ce critère est moins représentatif des meilleurs recettes car la majorité des recettes sont notés 4 ou plus. 
        De plus, des exemples de recettes très populaires mais avec notes en dessous de la médiane sont présents dans la dataframe ci-dessus
        (exemple : la recette "best banana bread" est notée 4,186 en moyenne).
        """

        st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].display_graph(
            explanation=explanation_graph_5
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].name}")

        conclusion_part_2 = """
        D'après cette analyse, deux critères peuvent définir la popularité d'une recette. 
        Tout d'abord, l'élément le plus discriminant est le nombre de commentaires par recettes 
        car seul très peu de recettes réussissent à attirer l'engagement des utilisateurs.
         
        Un second élément moins représentatif est la note moyenne permettant de supprimer les recettes dépréciées, 
        mais ne permettant pas de juger seul de l'attractivité d'une recette.

        Dans le reste de cette étude on se placera dans ces conditions : 
        - nombre de commentaires par recette : supérieur ou égale à 5
        - note moyenne : supérieur ou égale à 4
        """

        with st.container(border=True):
            st.write(conclusion_part_2)

        

        st.header("3️⃣ Caractéristiques des recettes populaires")
        

        explanation_graph_ = """
        **Observations :**
        - La majorité des recettes populaires sont des recettes courtes, avec une durée de préparation inférieure à 100 Durée de la recette (minutes).
        - Les recettes populaires ont tendance à avoir un nombre de commentaires plus élevé, avec une concentration autour de 1000 commentaires.

        **Interprétation :**
        - Les recettes courtes pourraient être **plus populaires** car elles sont **plus faciles et rapides à réaliser**.
        - Les recettes populaires génèrent plus de commentaires, ce qui peut indiquer un **engagement plus fort de la part des utilisateurs**.
        """

        st.session_state["locked_graphs"]["Duree recettes populaires"].display_graph(
            explanation=explanation_graph_
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Duree recettes populaires"].name}")

        st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].name}")

        st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"].name}")

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

        st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"].name}")
        
        
    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
