import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging
from utils.dbapi import DBapi
from class_dams import AdvanceStudy
import functions

def tracer_graphes():
    client_DB = DBapi()

    # nombre de recettes par années
    nb_recette_par_annee_df = client_DB.find_by_columns(
        ["recipe_id", "submitted", "rating"]
    )
    print(nb_recette_par_annee_df.head())
    nb_recette_par_annee_df["submitted"] = pd.to_datetime(
        nb_recette_par_annee_df["submitted"]
    )
    nb_recette_par_annee_df["rating"] = nb_recette_par_annee_df["rating"].apply(
        lambda x: ast.literal_eval(x)
    )

    nb_recette_par_annee_df["rating_count"] = nb_recette_par_annee_df["rating"].apply(
        len
    )
    nb_recette_par_annee_df["rating_mean"] = nb_recette_par_annee_df["rating"].apply(
        lambda x: sum(x) / len(x) if len(x) > 0 else 0
    )
    nb_recette_par_annee_df["year"] = nb_recette_par_annee_df["submitted"].dt.year
    nb_recette_par_annee_df["month"] = nb_recette_par_annee_df["submitted"].dt.month
    nb_recette_par_annee_df["submitted_by_month"] = (
        nb_recette_par_annee_df["submitted"].dt.to_period("M").dt.to_timestamp()
    )
    submissions_groupmonth = (
        nb_recette_par_annee_df["submitted_by_month"].value_counts().sort_index()
    )
    decomposition = sm.tsa.seasonal_decompose(
        submissions_groupmonth, model="additive", period=12
    )
    trend = pd.DataFrame(
        {
            "Date": decomposition.trend.index,  # X-axis: Time or index
            "Trend": decomposition.trend.values,  # Y-axis: Trend values
        }
    )
    nb_recette_par_annee_study = AdvanceStudy(
        dataframe=trend,
        key="1",
        name="Moyenne du nombre de recettes au cours du temps",
        axis_x="Date",
        axis_y="Trend",
        plot_type="plot",
    )
    st.session_state["locked_graphs"].append(nb_recette_par_annee_study)


def main():
    st.markdown("")
    if st.session_state["first_load"] == True:
        tracer_graphes()
        st.session_state["first_load"] = False

    for graph in st.session_state["locked_graphs"]:
        graph.display_graph()


if __name__ == "__main__":
    main()