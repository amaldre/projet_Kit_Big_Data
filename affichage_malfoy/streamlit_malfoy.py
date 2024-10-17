import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import ast
import time
from collections import Counter

PP_recipe = pd.read_csv("../data/PP_recipes.csv")
PP_users = pd.read_csv("../data/PP_users.csv")
RAW_recipes = pd.read_csv("../data/RAW_recipes.csv")
interactions_test = pd.read_csv("../data/interactions_test.csv")

############ definition of the functions

st.button("button")

############ Data analysis

### This is preliminary steps to sort the rows

max_calories = st.sidebar.slider('Calories', 0, 1000, 1000) # Slider for the calories ( in the left sidebar )
total_fat = st.sidebar.slider('total fat (%)', 0, 100, 10) # Slider for the calories ( in the left sidebar )
sugar = st.sidebar.slider('sugar (%consultant junior)', 0, 100, 0) # Slider for the calories ( in the left sidebar )
protein = st.sidebar.slider('protein (%)', 0, 100, 10) # Slider for the calories ( in the left sidebar )
# ingredients = st.text_input('Ingredients (seperate every ingredients with a ",")') # To obtain the differents ingredients

### First separate every nutritional informations

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

l_ingredient = list(RAW_recipes.ingredients)

# words_list = ingredients.split(',')

# ingredients_to_search = [word.strip() for word in words_list] # Put every ingredients in a vector (ex : ['basmati rice', 'water'])

# pattern = ''.join([f'(?=.*\\b{ingredient}\\b)' for ingredient in ingredients_to_search]) # Regex expression

# Extract the rows with the ingredients written by the user
# matching_rows = RAW_recipes[RAW_recipes['ingredients'].str.contains(pattern, case=False, na=False, regex=True)] 

# matching_rows["full_nutrition"] = matching_rows['nutrition'].apply(ast.literal_eval) # Because the nutrition column is written as a string
# Ex : [840.0,40.0] written as '[','8','4' etc..
# matching_rows["full_nutrition"] = matching_rows['full_nutrition'].apply(lambda x: x)
# matching_rows["calories"] = matching_rows['full_nutrition'].apply(lambda x: x[0]) # Extract the calories to sort later

# filtered_recipes = matching_rows[matching_rows['calories'] < calories] # Filter the recipes by the calories with the slider defined at the beginning

### After defining, we filter the recipes by the parameters

filtered_recipes = RAW_recipes[RAW_recipes['calories'] < max_calories]
filtered_recipes = filtered_recipes[RAW_recipes['total fat (%)'] < total_fat]
filtered_recipes = filtered_recipes[RAW_recipes['sugar (%)'] == sugar]
filtered_recipes = filtered_recipes[RAW_recipes['protein (%)'] < protein]

spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'powder'] # Common spices to exclude from list of ingredients
common_ingredients = ['water', 'flour', 'baking powder','cornstarch', 'sugar'] # Because water and flour don't have important nutritional values
alcohol = ['vodka', 'ice', 'beer']

### Taken from the correction of the TP, give the list of ingredients

l_ingredient = list(filtered_recipes.ingredients)
list_ingredient = []
for item in l_ingredient: 
    item = ast.literal_eval(item)
    for i in item: 
        list_ingredient.append(i)

### Filter the list of ingredients by the 2 lists defined below

filtered_strings_spices = [s for s in list_ingredient if not any(word in s for word in spices)]
filtered_strings = [s for s in filtered_strings_spices if not any(word in s for word in common_ingredients)]
filtered_strings = [s for s in filtered_strings if not any(word in s for word in alcohol)]

# print('There are {} unique ingredients'.format(len(set(list_ingredient))))
# print('There are {} unique ingredients without spices'.format(len(set(filtered_strings))))

### Take the most 5 common elements

element_counts = Counter(filtered_strings)
top_five = element_counts.most_common(5)
# print(top_five)
list_ing = []
for i in range (len(top_five)):
    list_ing.append(top_five[i][0])

# print(list_ing)

def contains_top_ingredients(ingredients):
    return any(ingredient in ingredients for ingredient in list_ing)

matching_rows = filtered_recipes[filtered_recipes['ingredients'].apply(contains_top_ingredients)]

st.title("For the 5 most common ingredients")
st.header("The 5 most common ingredients under {} calories are :".format(max_calories))
for i in range(len(list_ing)):
    st.text("> {}".format(list_ing[i]))

st.text(matching_rows['calories'].describe())

st.header("A list of recipes using those 5 ingredients")

st.dataframe(matching_rows.head())

st.header("A visualization of the nutritive aspects of the recipes using the 5 most common inrgedients")

f, axes = plt.subplots(1, 2, figsize=(18, 6))   

sns.boxplot(data=matching_rows, x='calories', ax=axes[0])
plt.title('Boxplot of the calories for the top 5 ingredients')
sns.kdeplot(matching_rows['calories'], ax=axes[1])
plt.title('Density plot of the calories for the top 5 ingredients')

st.pyplot(f)

### Now we can examine the top 20 ingredients

top_twenty = element_counts.most_common(20)
# print(top_twenty)
list_ing = []
for i in range (len(top_twenty)):
    list_ing.append(top_twenty[i][0])

# print(list_ing)

matching_rows = filtered_recipes[filtered_recipes['ingredients'].apply(contains_top_ingredients)]

st.title("For the 20 most common ingredients")
st.header("The 20 most common ingredients under {} calories are :".format(max_calories))
for i in range(len(list_ing)):
    st.text("> {}".format(list_ing[i]))

st.text(matching_rows['calories'].describe())

st.header("A list of recipes using those 5 ingredients")

st.dataframe(matching_rows.head())

st.header("A visualization of the nutritive aspects of the recipes using the 5 most common inrgedients")

f, axes = plt.subplots(1, 2, figsize=(18, 6))

sns.boxplot(data=matching_rows, x='calories', ax=axes[0])
plt.title('Boxplot of the calories for the top 20 ingredients')
sns.kdeplot(matching_rows['calories'], ax=axes[1])
plt.title('Density plot of the calories for the top 20 ingredients')

st.pyplot(f)

############ Display of the app

# st.title("Display of the recipe")

# st.dataframe(matching_rows.head())

# recipe_1 = filtered_recipes.head(1)

# recipe_1_description = (recipe_1["steps"].values[0])
# cleaned_text = recipe_1_description.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
# cleaned_text = cleaned_text.replace(",", "\n")
# instructions_string = cleaned_text.strip()

# st.header("Steps of the first recipe")

# st.text(instructions_string)
