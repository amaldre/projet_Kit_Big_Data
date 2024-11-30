import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import date
from utils.load_csv import load_numerical_df, load_trend
from utils.classes import bivariateStudy
import pandas as pd
import ast


st.set_page_config(layout="wide")
st.title("DataViz")

st.markdown("Dans cette page, parcourez librement les données")


@st.cache_data
def import_df(df_path):
    recipes_df = pd.read_csv(df_path)
    return recipes_df


@st.cache_data
def merge_df(df1, df2, column):
    return pd.merge(df1, df2, on=column)


if "graph" not in st.session_state:
    st.session_state["graph"] = []

if "numerical_df" not in st.session_state:
    st.session_state["numerical_df"] = None

if "first_load_dataviz" not in st.session_state:
    st.session_state["first_load_dataviz"] = True






def main():
    # nombre de recettes par années
    axis_x_list = [
        "minutes",
        "n_steps",
        "comment_count",
        "ingredient_count",
        "submitted",
    ]
    axis_y_list = ["comment_count", "mean_rating"]
    filters = ["comment_count", "mean_rating", "submitted"]

    if st.session_state["first_load_dataviz"] == True:
        print("first load dataviz", st.session_state["first_load_dataviz"])
        st.session_state["numerical_df"] =load_numerical_df()
        st.session_state["first_load_dataviz"] = False

    for i, graph in enumerate(st.session_state["graph"]):

        if graph.delete == True:
            st.session_state["graph"].remove(graph)
            print("remove", len(st.session_state["graph"]))
        else:
            graph.display_graph(free=True)

    if st.button("Add Graph"):
        name = f"graph {len(st.session_state["graph"]) + 1}"
        study = bivariateStudy(dataframe=st.session_state["numerical_df"], axis_x_list=axis_x_list, axis_y_list=axis_y_list, filters=filters, key=name, plot_type = "scatter")
        st.session_state["graph"].append(study)
        print("add",len(st.session_state["graph"]))
        st.rerun()      

if __name__ == "__main__":
    main()
