import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging

from class_block_st import Block

with st.form('form2'):

    spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'garlic'] # Common spices to exclude from list of ingredients
    common_ingredients = ['water', 'flour', 'baking powder','cornstarch'] # Because water and flour don't have important nutritional values
    alcohol = ['vodka', 'ice', 'beer']

    filtre = spices+common_ingredients+alcohol

    RAW_recipes = pd.read_csv("../data/RAW_recipes.csv")

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

    list_option = ['calories','total fat (%)', 'sugar (%)']

    arg = st.selectbox(label = 'Choose', options = list_option)

    if arg == 'calories':
        valeur = 1000
    else:
        valeur = 20

    my_block = Block(RAW_recipes, arg, valeur, filtre)

    if 'graphs' not in st.session_state:
        st.session_state.graphs = []

    if st.form_submit_button('$+$'):
        if 'graph' not in st.session_state:
            fig = my_block.graph()
            st.session_state.graphs.append(fig)
            st.write("Voici les graphes sauvegardés dans session_state :")
            for graph in st.session_state.graphs:
                st.pyplot(graph)