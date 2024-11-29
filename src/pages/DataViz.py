import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import date
from utils.dbapi import DBapi
from utils.classes import Study
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

def load_numerical_df():
    client_DB = DBapi()
    columns = ["recipe_id", "minutes", "submitted", "n_steps", "date", "rating", "ingredients_replaced", "cleaned_name"]
    numerical_df = client_DB.find_by_columns(columns)

    numerical_df['submitted'] = pd.to_datetime(numerical_df['submitted'])
    numerical_df['rating'] = numerical_df['rating'].apply(lambda x: ast.literal_eval(x))

    numerical_df['comment_count'] = numerical_df['rating'].apply(len)
    numerical_df['mean_rating'] = numerical_df['rating'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)
    numerical_df['ingredient_count'] = numerical_df['ingredients_replaced'].apply(len)

    numerical_df = numerical_df[["recipe_id",'mean_rating','comment_count',"minutes", "submitted", "n_steps", "date", "rating", "ingredients_replaced", "ingredient_count", "cleaned_name"]]

    st.session_state["numerical_df"] =numerical_df




def main():
    # nombre de recettes par années
    axis_x_list= ["minutes", "n_steps", "comment_count", "ingredient_count", "submitted"]
    axis_y_list= ["comment_count","mean_rating"]
    filters = ["comment_count","mean_rating","submitted"]

    if st.session_state["first_load_dataviz"] == True:
        print("first load dataviz", st.session_state["first_load_dataviz"])
        load_numerical_df()

        st.session_state["first_load_dataviz"] = False
    
        

    


    

    for i, graph in enumerate(st.session_state["graph"]):
        
        if graph.delete==True:
            st.session_state["graph"].remove(graph)
            print("remove",len(st.session_state["graph"]))
        else:
            graph.display_graph(free=True)
    
    if st.button("Add Graph"):
        name = f"graph {len(st.session_state["graph"]) + 1}"
        study = Study(dataframe=st.session_state["numerical_df"], axis_x_list=axis_x_list, axis_y_list=axis_y_list, filters=filters, key=name, plot_type = "scatter")
        st.session_state["graph"].append(study)
        print("add",len(st.session_state["graph"]))
        st.rerun()
            
    
    
        

if __name__ == "__main__":
    main()