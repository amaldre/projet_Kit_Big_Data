import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter
import logging

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