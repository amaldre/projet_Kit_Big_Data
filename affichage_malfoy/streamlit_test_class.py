import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging

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

st.markdown("""
Ce graphique illustre une tendance à la baisse constante de la popularité des recettes sur Food.com depuis 2000. 
Une exploration des caractéristiques des recettes populaires est nécessaire pour mieux comprendre ce phénomène.
""")

st.subheader("✨ Qu'est-ce qui rend une recette intemporelle ?")

st.markdown("""
Les recettes les plus populaires ont souvent des temps de préparation modérés, indiquant un équilibre entre simplicité et raffinement. 
Analysons ces paramètres plus en détail pour dégager des tendances exploitables.
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