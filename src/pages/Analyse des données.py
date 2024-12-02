import streamlit as st
from utils.classes import bivariateStudy
from pandas import Timestamp
from utils.load_csv import compute_trend, load_df


st.set_page_config(layout="wide")
st.title("Analyse des data")

if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = load_df("data/cloud_df.csv")


if "first_load" not in st.session_state:
    st.session_state["first_load"] = True

if "locked_graphs" not in st.session_state:
    st.session_state["locked_graphs"] = []




def main():
    st.markdown("")
    if st.session_state["first_load"] == True :
        trend=compute_trend(st.session_state["recipes_df"])
        nb_recette_par_annee_study = bivariateStudy(dataframe=trend, key = "1", name = "Moyenne du nombre de recettes au cours du temps", axis_x="Date", axis_y="Trend", plot_type="plot", default_values={"Date": (Timestamp('1999-08-01 00:00:00'), Timestamp('2018-12-1 00:00:00')), "Trend": (3, 2268), "chosen_filters":[]})
        st.session_state["locked_graphs"].append(nb_recette_par_annee_study)

        min_popular_recipes = bivariateStudy(dataframe=st.session_state["recipes_df"], key="2", name="durée recettes populaires", axis_x="minutes", axis_y="comment_count", filters=['mean_rating'], plot_type="scatter", default_values={"minutes": (1, 279), "comment_count": (100, 1613), "mean_rating":(4, 5), "chosen_filters":['mean_rating']})
        st.session_state["locked_graphs"].append(min_popular_recipes)

        # Example of how to add a new graph
        # new_graph= bivariateStudy(dataframe=st.session_state["recipes_df"], key="2", name="durée recettes populaires", axis_x="minutes", axis_y="comment_count", filters=['mean_rating'], plot_type="scatter", default_values={"minutes": (1, 279), "comment_count": (100, 1613), "mean_rating":(4, 5), "chosen_filters":['mean_rating']})
        # st.session_state["locked_graphs"].append(min_popular_recipes)


        st.session_state["first_load"] = False


    for graph in st.session_state["locked_graphs"]:
        graph.display_graph()


if __name__ == "__main__":
    main()
