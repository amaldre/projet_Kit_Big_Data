import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging
from class_dams import Study
from class_block_st import Block

st.set_page_config(layout="wide")
st.title("Data Visualiser")

@st.cache_data
def import_df(df_path):
    recipes_df = pd.read_csv(df_path)
    return recipes_df

@st.cache_data
def merge_df(df1, df2, column):
    return pd.merge(df1, df2, on=column)

if "graph" not in st.session_state:
    st.session_state["graph"] = []

if "filters" not in st.session_state:
    st.session_state["filters"] = []

def main():

    col1, col2, _, _, _, _, _, _, _, _ = st.columns(10)

    with col1:
        refresh_button = st.button("refresh")
    with col2:
        add_graph_button = st.button("Add Graph")

    if refresh_button:
        st.rerun()

    recipes_df = import_df("../data/recipes_explicit_nutriments.csv")
    mean_rating_df = import_df("../data/mean_ratings.csv")
    mean_rating_df.rename(columns={"recipe_id":"id"}, inplace=True)
    idx_with_max_value = recipes_df["calories"].values.argmax()
    recipes_df = recipes_df.drop(index=idx_with_max_value)
    dataframe = merge_df(recipes_df,mean_rating_df,"id")

    axis_x_list = ["count_total","mean_rating","calories","total fat (%)","sugar (%)","sodium (%)","protein (%)","saturated fat (%)","carbohydrates (%)"]
    filters = ["count_total","mean_rating","calories","total fat (%)","sugar (%)","sodium (%)","protein (%)","saturated fat (%)","carbohydrates (%)"]

    if add_graph_button:
        name = f"graph {len(st.session_state["graph"]) + 1}"
        study = Study(dataframe, axis_x_list, filters, name)
        st.session_state["graph"].append(study)
        print("add",len(st.session_state["graph"]))

    for i, graph in enumerate(st.session_state["graph"]):
        
        if graph.delete==True:
            st.session_state["graph"].remove(graph)
            print("remove",len(st.session_state["graph"]))
        else:
            graph.display_graph()

if __name__ == "__main__":
    main()