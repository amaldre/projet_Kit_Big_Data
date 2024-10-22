import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from classes import Study


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


def main():

    print("début",len(st.session_state["graph"]))
    if st.button("refresh"):
        st.rerun()

    recipes_df = import_df("data/recipes_explicit_nutriments.csv")
    mean_rating_df = import_df("data/mean_ratings.csv")
    mean_rating_df.rename(columns={"recipe_id":"id"}, inplace=True)
    idx_with_max_value = recipes_df["calories"].values.argmax()
    recipes_df = recipes_df.drop(index=idx_with_max_value)
    dataframe = merge_df(recipes_df,mean_rating_df,"id")



    axis_x_list = ["count_total","mean_rating"]
    axis_y_list = ["calories","n_steps","minutes","n_ingredients","mean_rating","count_total"]
    filters = ["count_total","mean_rating"]

    

    if st.button("Add Graph"):
        name = f"graph {len(st.session_state["graph"]) + 1}"
        study = Study(dataframe, axis_x_list, axis_y_list, filters, name)
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