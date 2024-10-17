import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging

from class_block_st import Block

spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'garlic'] # Common spices to exclude from list of ingredients
common_ingredients = ['water', 'flour', 'baking powder','cornstarch'] # Because water and flour don't have important nutritional values
alcohol = ['vodka', 'ice', 'beer']

filtre = spices+common_ingredients+alcohol

@st.cache_data
def load_data():
    # Simuler un chargement de données lourd
    data = pd.read_csv("../../data/RAW_recipes.csv")
    return data

RAW_recipes = load_data()

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

if 'arg' not in st.session_state:
    st.session_state.arg = 'calories'
if 'valeur' not in st.session_state:
    st.session_state.valeur = 0

with st.form('form1'):
    arg = st.selectbox(label='Choose', options = list_option, key='arg')
    submit_button1 = st.form_submit_button('Set Argument')

with st.form('form2'):
    if st.session_state.arg == 'calories':
        valeur = st.slider('Valeur', 0, 1000, st.session_state.valeur, 500)
    else:
        valeur = st.slider('Valeur', 0, 100, st.session_state.valeur, 50)
    submit_button = st.form_submit_button('$+$')
    if submit_button:
        st.session_state.valeur = valeur

if 'graphs' not in st.session_state:
    st.session_state.graphs = []

if submit_button:
    my_block = Block(RAW_recipes, arg, valeur, filtre)
    fig = my_block.graph(my_block.dataframe, my_block.argument, valeur, filtre)
    st.session_state.graphs.append(fig)

#if st.session_state.graphs:
    #st.write("Voici les graphes sauvegardés dans session_state :")
    #for graph in st.session_state.graphs:
        #st.pyplot(graph)

if st.session_state.graphs:
    st.write("Graph à supprimer :")

    graphs_to_display = st.session_state.graphs.copy()

    for idx, fig in enumerate(graphs_to_display):
        if st.button(f'Supprimer le graphique {idx + 1}', key=f'remove_{idx}'):
            st.session_state.graphs.pop(idx)
            st.rerun()
            break
    if st.session_state.graphs:
        st.write("Graphiques affichés :")
        for remaining_fig in st.session_state.graphs:
            st.pyplot(remaining_fig)
else:
    st.write("Aucun graphique sauvegardé.")