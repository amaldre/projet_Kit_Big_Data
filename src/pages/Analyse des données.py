import streamlit as st
from utils.dbapi import DBapi
from utils.classes import bivariateStudy
import pandas as pd
import ast
from utils.load_csv import load_trend, load_numerical_df

st.set_page_config(layout="wide")
st.title("Analyse des data")

if "first_load" not in st.session_state:
    st.session_state["first_load"] = True

if "locked_graphs" not in st.session_state:
    st.session_state["locked_graphs"] = []




def main():
    st.markdown("")
    if st.session_state["first_load"] == True :
        trend=load_trend()
        nb_recette_par_annee_study = bivariateStudy(dataframe=trend, key = "1", name = "Moyenne du nombre de recettes au cours du temps", axis_x="Date", axis_y="Trend", plot_type="plot")
        st.session_state["locked_graphs"].append(nb_recette_par_annee_study)


    for graph in st.session_state["locked_graphs"]:
        graph.display_graph()


if __name__ == "__main__":
    main()
