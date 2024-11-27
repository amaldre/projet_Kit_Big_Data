import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging
import statsmodels.api as sm

from pymongo import MongoClient, errors
import dotenv
import os
import logging
import sys
from pathlib import Path

from dbapi import DBapi

db_api = DBapi()



df_g['description'] = df_g['description'].fillna(df_g['name'])
df_g = df_g.dropna(subset=['name'])
df_g['contributor_id'] = df_g.contributor_id.astype('category')
df_g['recipe_id'] = df_g.recipe_id.astype('category')
df_g  = df_g.sort_values('minutes',ascending=False)
df_g = df_g.drop(df_g['minutes'].nlargest(2).index)
df_g  = df_g.sort_values('minutes',ascending=True)
idx = df_g.index[df_g['minutes'] < 2].tolist()
df_g = df_g.drop(idx)
df_g  = df_g.sort_values('n_steps',ascending=True)
df_g = df_g.drop(df_g['n_steps'].idxmax())
df_g  = df_g.sort_values('n_steps',ascending=True)
df_g = df_g.drop(df_g['steps'].idxmin())
df_g  = df_g.sort_values('n_ingredients',ascending=False)
df_g = df_g.drop(df_g['n_steps'].idxmax())
df_g  = df_g.sort_values('n_ingredients',ascending=True)
df_g['year'] = df_g['submitted'].dt.year
df_g['month'] = df_g['submitted'].dt.month
df_g['day'] = df_g['submitted'].dt.day
df_g['day_of_week'] = df_g['submitted'].dt.day_name()
df_g['submitted_by_week']=df_g['submitted'].dt.to_period('W').dt.to_timestamp()
df_g['submitted_by_month']=df_g['submitted'].dt.to_period('M').dt.to_timestamp()
df_g['n_comments'] = df_g['review'].apply(len)
df_g = df_g.sort_values(by='n_comments', ascending=False)

submissions_per_year = df_g['submitted'].value_counts().sort_index()
submissions_per_month = df_g['month'].value_counts().sort_index()

submissions_group_week = df_g['submitted_by_week'].value_counts().sort_index()
submissions_groupmonth = df_g['submitted_by_month'].value_counts().sort_index()

decomposition = sm.tsa.seasonal_decompose(submissions_group_week, model='additive', period=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid


decomposition = sm.tsa.seasonal_decompose(submissions_groupmonth, model='additive', period=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid



st.set_page_config(
    page_title="Analyse de la Perte de Popularité de Food.com",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📉 Food.com : Diagnostiquer la Perte de Popularité")

st.markdown("""
Bienvenue dans cette application d'analyse interactive.  
Le site **Food.com**, autrefois une référence pour les amateurs de cuisine, est en perte de vitesse, comme le montrent les tendances au fil des années.  
Notre objectif est de comprendre les causes de ce déclin en examinant les **trends** et les caractéristiques des recettes les plus populaires.  
**Objectif final :** Identifier des leviers pour revitaliser Food.com et regagner sa communauté culinaire.
""")

st.subheader("📊 Évolution de la popularité des recettes au fil des ans")

fig, ax = plt.subplots()
submissions_per_year.plot(kind='line', title='Submitted')
ax.set_xlabel('Année')
ax.set_ylabel('Nombre de recettes')
st.pyplot(fig)

st.markdown("""
Ce graphique illustre une tendance à la baisse constante de la popularité des recettes sur Food.com depuis 2010. 
Une exploration des caractéristiques des recettes populaires est nécessaire pour mieux comprendre ce phénomène.
""")

st.subheader("✨ Est ce que les recettes les plus populaires étaient postées entre 2008 et 2010 ?")

n_largest = df_g.nlargest(5, 'n_comments')

fig, ax = plt.subplots()
for i in range(len(n_largest)):
    plt.hist(df_g.loc[n_largest.index[i]]['date'], bins=50, edgecolor='black', alpha=0.5)
plt.title('Top 5 Recettes commentées')
plt.xlabel('Date')
plt.ylabel('n_comments')
st.pyplot(fig)

st.markdown("""
Les recettes les plus populaires ont bien été postées entre 2008 et 2010, ce qui montre que l'intérêt pour le site a bien baissé avec le nombre de contributions.
On remarque quand même qu'une recette a été populaire en 2018.
""")

st.subheader("🍲 L'évolution des préférences culinaires")

st.markdown("""
Les tendances des catégories culinaires évoluent avec le temps, reflétant les goûts et préférences des utilisateurs. 
Explorer ces données peut nous aider à identifier des opportunités pour innover sur Food.com.
""")

st.markdown("""
---
### 🎯 Que pouvons-nous apprendre de ces données ?
Passez à la section suivante pour découvrir des **insights** et des **recommandations** basées sur ces analyses !
""")

if st.button("Commencer l'analyse"):
    st.write("🚀 Passons à l'analyse détaillée !")

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("style.css")

# st.title("Custom Styled Streamlit App")
# st.write("This app has a custom background and text color!")

# page_background = """
# <style>
# .stApp {
#     background-color: #FF0000; /* Fond rouge pour toute la page */
#     color: #FFFFFF; /* Texte en blanc pour plus de lisibilité */
# }
# .css-1d391kg {  /* Classe de la sidebar, peut varier selon la version de Streamlit */
#     background-color: #FF0000; /* Rouge pour la sidebar */
#     color: #FFFFFF; /* Texte en blanc pour la sidebar */
# }
# </style>
# </style>
# """

# # Injecter le CSS dans la page
# st.markdown(page_background, unsafe_allow_html=True)