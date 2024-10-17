import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter

spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'garlic'] # Common spices to exclude from list of ingredients
common_ingredients = ['water', 'flour', 'baking powder','cornstarch'] # Because water and flour don't have important nutritional values
alcohol = ['vodka', 'ice', 'beer']

class Block:

    def __init__(self, dataframe, argument, valeur, filtre):

        self.dataframe = dataframe
        self.argument = argument
        self.valeur = valeur
        self.filtre = filtre

        pass
    
    def filtre_dataframe(_self, dataframe, argument, valeur, filtre):

        #dataframe = self.dataframe
        #argument = self.argument
        #valeur = self.valeur
        #filtre = self.filtre
        list_ing = []
        list_ingredient = []

        filtered_recipes = dataframe[dataframe[argument] < valeur]
        l_ingredient = list(filtered_recipes.ingredients_cleaned)
        for item in l_ingredient: 
            item = ast.literal_eval(item)
            for i in item: 
                list_ingredient.append(i)
        filtered_strings = [s for s in list_ingredient if not any(word in s for word in filtre)]
        element_counts = Counter(filtered_strings)
        top_five = element_counts.most_common(5)
        for i in range (len(top_five)):
            list_ing.append(top_five[i][0])
        
        return filtered_recipes, list_ing
    
    def top_ing(_self, filtered_recipes, list_ing):

        #filtered_recipes, list_ing = self.filtre_dataframe()

        def contains_top_ingredients(ingredients):
            return any(ingredient in ingredients for ingredient in list_ing)
        
        matching_rows = filtered_recipes[filtered_recipes['ingredients_cleaned'].apply(contains_top_ingredients)].copy()
        
        return matching_rows

    @st.cache_data
    def graph(_self, dataframe, argument, valeur, filtre):

        #dataframe = self.dataframe
        #argument = self.argument
        #valeur = self.valeur

        filtered_recipes, list_ing = _self.filtre_dataframe(dataframe, argument, valeur, filtre)

        matching_rows = _self.top_ing(filtered_recipes, list_ing)

        f, axes = plt.subplots(1, 2, figsize=(18, 6))
        sns.boxplot(data=matching_rows, x='calories', ax=axes[0])
        axes[0].set_title('Boxplot of the calories for the top 5 ingredients')
        sns.kdeplot(matching_rows['calories'], ax=axes[1])
        axes[1].set_title('Density plot of the calories for the top 5 ingredients')

        return f