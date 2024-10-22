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

def create_slider_from_df(df,column):
    min = math.floor(df[column].min())
    max = math.ceil(df[column].max())
    print(min,max)
    return st.slider(label = f"range for {column}", min_value=min, max_value=max, value=(min,max), step=1)

def get_data_points(merged_df, axis_x, axis_y, range_axis_x, range_axis_y):
    df = merged_df[[axis_x,axis_y,"recipe_id"]].sort_values(by=axis_x)
    df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]
    df = df[(df[axis_y] >= range_axis_y[0]) & (df[axis_y] <= range_axis_y[1])]
    return df[axis_x].values, df[axis_y].values, df["recipe_id"].values


# def main():
#     recipes_df = import_df("data/recipes_explicit_nutriments.csv")
#     mean_rating_df = import_df("data/mean_ratings.csv")
#     recipes_df.rename(columns={"id":"recipe_id"}, inplace=True)
#     idx_with_max_value = recipes_df["calories"].values.argmax()
#     recipes_df = recipes_df.drop(index=idx_with_max_value)
#     merged_df = merge_df(recipes_df,mean_rating_df,"recipe_id")

#     axis_y = st.selectbox(label="axis_y", options= ["count_total","mean_rating"])
#     axis_x = st.selectbox(label="axis_x", options= ["calories","n_steps","minutes","n_ingredients"])
    
#     range_axis_y = create_slider_from_df(mean_rating_df, axis_y)
#     range_axis_x = create_slider_from_df(recipes_df, axis_x)

#     # Generate data
#     x, y, recipes_id = get_data_points(merged_df, axis_x, axis_y, range_axis_x, range_axis_y)
    

#     col = st.columns([1,3,1])
#     with col[1]:
#     # Create a figure
#         fig, ax = plt.subplots(figsize=(10,6))
#         ax.scatter(x, y, s=0.5)

#         # Display Matplotlib figure in Streamlit
#         st.pyplot(fig)

#         st.write(f"number of recipes : {len(x)}")

#     display_df = merged_df[merged_df['recipe_id'].isin(recipes_id)]
#     display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
#     with st.expander("The 10 recipes with the most comments (with current filters)"):
#         st.dataframe(display_df,hide_index=True)

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