import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import date
from utils.classes import bivariateStudy
import pandas as pd
import ast
from utils.load_csv import load_df


st.set_page_config(layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

st.title("DataViz")

st.markdown("Dans cette page, parcourez librement les données")


if "graph" not in st.session_state:
    st.session_state["graph"] = []

if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = load_df("data/cloud_df.csv")


def main():
    # nombre de recettes par années
    axis_x_list = [
        "minutes",
        "n_steps",
        "comments_count",
        "ingredient_count",
        "submitted",
    ]
    axis_y_list = ["comment_count", "mean_rating"]
    filters = ["comment_count", "mean_rating", "submitted"]


    for i, graph in enumerate(st.session_state["graph"]):

        if graph.delete == True:
            st.session_state["graph"].remove(graph)
            print("remove", len(st.session_state["graph"]))
        else:
            graph.display_graph(free=True)

    if st.button("Add Graph"):
        name = f"graph {len(st.session_state["graph"]) + 1}"
        study = bivariateStudy(dataframe=st.session_state["recipes_df"], axis_x_list=axis_x_list, axis_y_list=axis_y_list, filters=filters, key=name, plot_type = "scatter")
        st.session_state["graph"].append(study)
        print("add",len(st.session_state["graph"]))
        st.rerun()      

if __name__ == "__main__":
    main()
