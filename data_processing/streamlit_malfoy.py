import streamlit as st
import pandas as pd
import ast
import time

PP_recipe = pd.read_csv("PP_recipes.csv")
PP_users = pd.read_csv("PP_users.csv")
RAW_recipes = pd.read_csv("RAW_recipes.csv")
interactions_test = pd.read_csv("interactions_test.csv")

############ definition of the functions



############ Data analysis

### This is preliminary steps to sort the rows

calories = st.sidebar.slider('Calories', 0, 1000, 500) # Slider for the calories ( in the left sidebar )
ingredients = st.text_input('Ingredients (seperate every ingredients with a ",")') # To obtain the differents ingredients

words_list = ingredients.split(',')

ingredients_to_search = [word.strip() for word in words_list] # Put every ingredients in a vector (ex : ['basmati rice', 'water'])

pattern = ''.join([f'(?=.*\\b{ingredient}\\b)' for ingredient in ingredients_to_search]) # Regex expressio

# Extract the rows with the ingredients written by the user
matching_rows = RAW_recipes[RAW_recipes['ingredients'].str.contains(pattern, case=False, na=False, regex=True)] 

matching_rows["full_nutrition"] = matching_rows['nutrition'].apply(ast.literal_eval) # Because the nutrition column is written as a string
# Ex : [840.0,40.0] written as '[','8','4' etc..
matching_rows["full_nutrition"] = matching_rows['full_nutrition'].apply(lambda x: x)
matching_rows["calories"] = matching_rows['full_nutrition'].apply(lambda x: x[0]) # Extract the calories to sort later

filtered_recipes = matching_rows[matching_rows['calories'] < calories] # Filter the recipes by the calories with the slider defined at the beginning

############ Display of the app

st.title("Display of the recipe")

st.dataframe(filtered_recipes.head())

recipe_1 = filtered_recipes.head(1)

recipe_1_description = (recipe_1["steps"].values[0])
cleaned_text = recipe_1_description.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
cleaned_text = cleaned_text.replace(",", "\n")
instructions_string = cleaned_text.strip()

st.header("Steps of the first recipe")

st.text(instructions_string)
