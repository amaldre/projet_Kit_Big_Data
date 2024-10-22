import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging

from class_block_st import Block
import functions

@st.cache_data
def load_data(df_path):
    data = pd.read_csv(df_path)
    return data

RAW_recipes = load_data("../data/RAW_recipes.csv")

RAW_recipes[['calories','total fat (%)','sugar (%)','sodium (%)','protein (%)','saturated fat (%)','carbohydrates (%)']] = RAW_recipes.nutrition.str.split(",",expand=True)
RAW_recipes['calories'] = RAW_recipes['calories'].apply(lambda x: x.replace('[','')) 
RAW_recipes['carbohydrates (%)']= RAW_recipes['carbohydrates (%)'].apply(lambda x: x.replace(']',''))

RAW_recipes['calories'] = RAW_recipes['calories'].apply(ast.literal_eval)
RAW_recipes['total fat (%)'] = RAW_recipes['total fat (%)'].apply(ast.literal_eval)
RAW_recipes['sugar (%)'] = RAW_recipes['sugar (%)'].apply(ast.literal_eval)
RAW_recipes['sodium (%)'] = RAW_recipes['sodium (%)'].apply(ast.literal_eval)
RAW_recipes['protein (%)'] = RAW_recipes['protein (%)'].apply(ast.literal_eval)
RAW_recipes['saturated fat (%)'] = RAW_recipes['saturated fat (%)'].apply(ast.literal_eval)
RAW_recipes['carbohydrates (%)'] = RAW_recipes['carbohydrates (%)'].apply(ast.literal_eval)
RAW_recipes['ingredients_cleaned'] = RAW_recipes['ingredients'].str.lower().str.strip()

spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'garlic'] # Common spices to exclude from list of ingredients
common_ingredients = ['water', 'flour', 'baking powder','cornstarch'] # Because water and flour don't have important nutritional values
alcohol = ['vodka', 'ice', 'beer']
filtre = spices+common_ingredients+alcohol

list_option = ['calories','total fat (%)', 'sugar (%)']
list_df = ['RAW_recipes','RAW_recipes']

with st.form('form_df'):
    df_choose = st.selectbox(label='Choose', options = list_df, key='df_choose')
    submit_button1 = st.form_submit_button('Set Dataframe')

functions.main(RAW_recipes, list_option, filtre)