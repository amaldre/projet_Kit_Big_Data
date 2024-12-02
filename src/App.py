import streamlit as st
import pandas as pd
from utils.load_csv import load_df


if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = load_df("data/cloud_df.csv")

st.title("Mange ta main")

st.markdown(
    "Page d'intro expliquant le projet et le but de l'application i.e. son fil rouge "
)
