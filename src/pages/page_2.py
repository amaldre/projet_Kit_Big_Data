import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging
from utils.classes import AdvancedStudy
from utils.load_csv import load_df

st.set_page_config(layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

st.title("Data Visualiser")

@st.cache_data
def import_df(df_path):
    recipes_df = pd.read_csv(df_path)
    return recipes_df

if "graph_advanced" not in st.session_state:
    st.session_state["graph_advanced"] = []

if "filters_advanced" not in st.session_state:
    st.session_state["filters_advanced"] = []

if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = load_df("data/cloud_df.csv")

def main():

    col1, col2, _, _, _, _, _, _, _, _ = st.columns(10)

    with col1:
        refresh_button = st.button("refresh")
    with col2:
        add_graph_button = st.button("Add Graph")

    if refresh_button:
        st.rerun()

    axis_x_list = ["calories","mean_rating","comment_count","n_steps","ingredients_replaced","techniques"]
    filters = ["calories","mean_rating","comment_count","n_steps"]

    if add_graph_button:
        name = f"{len(st.session_state["graph_advanced"]) + 1}"
        study = AdvancedStudy(st.session_state["recipes_df"], axis_x_list, filters, name)
        st.session_state["graph_advanced"].append(study)
        print("add",len(st.session_state["graph_advanced"]))

    for i, graph in enumerate(st.session_state["graph_advanced"]):
        
        if graph.delete==True:
            st.session_state["graph_advanced"].remove(graph)
            print("remove",len(st.session_state["graph_advanced"]))
        else:
            graph.display_graph()

if __name__ == "__main__":
    main()