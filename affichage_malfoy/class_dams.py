import streamlit as st
import math
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter

class Study:

    def __init__(self, dataframe, axis_x_list, filters, key):
        # Attributs de la classe
        self.dataframe = dataframe
        self.axis_x_list = axis_x_list
        self.filters = filters
        self.axis_x = None
        self.range_axis_x = None
        self.key = key
        self.delete = False

    def __del__(self):
        return

    # Méthode d'affichage des attributs
    def print_self(self):
        print(
            self.axis_x_list,
            self.axis_x,
            self.range_axis_x,
            self.key)


    def __set_axis(self):
        axis_x = st.selectbox(label=f"graph {self.key}", options = self.axis_x_list, key=f"{self.key}_axis_x")
        return axis_x
    
    def __create_slider_from_df(self, df,column):
        min = math.floor(df[column].min())
        max = math.ceil(df[column].max())
        return st.slider(label = f"range for {column}", min_value=min, max_value=max, value=(min,max), step=1, key=f"{self.key}_slider_{column}")

    def get_data_points(self, df, axis_x, range_axis_x, chosen_filters, range_filters,):
        columns = [axis_x,"id"] + [filtre for filtre in chosen_filters if (filtre != axis_x)]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]
        if len(chosen_filters)>0:
            for i,filter in enumerate(chosen_filters):
                df = df[(df[filter] >= range_filters[i][0]) & (df[filter] <= range_filters[i][1])]
        return df[axis_x].values, df["id"].values
    

    def __set_range_axis(self):
        range_axis_x = self.__create_slider_from_df(self.dataframe, self.axis_x)
        return range_axis_x

    def __filters(self, axis_x):
        filters = [filtre for filtre in self.filters if (filtre != axis_x)]
        chosen_filters = st.sidebar.multiselect(label =f"filtre pour le graph {self.key}", options=filters, key=f"{self.key}_chosen_filters")
        print(chosen_filters)
        range_filters = []
        for filter in chosen_filters:
            min = math.floor(self.dataframe[filter].min())
            max = math.ceil(self.dataframe[filter].max())
            range = st.sidebar.slider(filter, min_value=min, max_value=max, value=(min,max), key=f"{self.key}_range_{filter}")
            print(range)
            range_filters.append(range)
            print(range_filters)
        print(range_filters)
        return chosen_filters,range_filters
    
    def filtre_top_ing(self, df, nb_top_ing):
        
        spices = ['salt', 'garlic', 'pepper', 'paprika', 'basil', 'lime', 'cumin', 'garlic'] # Common spices to exclude from list of ingredients
        common_ingredients = ['water', 'flour', 'baking powder','cornstarch'] # Because water and flour don't have important nutritional values
        alcohol = ['vodka', 'ice', 'beer']
        filtre_ing = spices+common_ingredients+alcohol

        l_ingredient = list(df.ingredients)
        list_ingredient = []
        for item in l_ingredient: 
            item = ast.literal_eval(item)
            for i in item: 
                list_ingredient.append(i)

        filtered_strings = [s for s in list_ingredient if not any(word in s for word in filtre_ing)]

        element_counts = Counter(filtered_strings)
        top_ing = element_counts.most_common(nb_top_ing)
        print(top_ing)
        list_ing = []
        for i in range (len(top_ing)):
            list_ing.append(top_ing[i][0])

        def contains_top_ingredients(ingredients):
            return any(ingredient in ingredients for ingredient in list_ing)

        matching_rows = df[df['ingredients'].apply(contains_top_ingredients)].copy()

        return matching_rows, list_ing
    
    # Pour les differents types de graphes
    def graph_normal(self, x, recipes_id):
        col = st.columns([1,3,1])
        with col[1]:
            fig, ax = plt.subplots(figsize=(10,6))
            ax.plot(x, marker='o', markersize=0.5)
            st.pyplot(fig)
            st.write(f"number of recipes : {len(x)}")
        display_df = self.dataframe[self.dataframe['id'].isin(recipes_id)]
        display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
        with st.expander("The 10 recipes with the most comments (with current filters)"):
            st.dataframe(display_df,hide_index=True)
    
    def graph_boxplot(self, x, recipes_id):
        col = st.columns([1,3,1])
        with col[1]:
            fig, ax = plt.subplots(figsize=(10,6))
            sns.boxplot(data=x, ax=ax)
            st.pyplot(fig)
            st.write(f"number of recipes : {len(x)}")
        display_df = self.dataframe[self.dataframe['id'].isin(recipes_id)]
        display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
        with st.expander("The 10 recipes with the most comments (with current filters)"):
            st.dataframe(display_df,hide_index=True)
    
    def graph_density(self, x, recipes_id):
        col = st.columns([1,3,1])
        with col[1]:
            fig, ax = plt.subplots(figsize=(10,6))
            sns.kdeplot(data=x, ax=ax)
            st.pyplot(fig)
            st.write(f"number of recipes : {len(x)}")
        display_df = self.dataframe[self.dataframe['id'].isin(recipes_id)]
        display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
        with st.expander("The 10 recipes with the most comments (with current filters)"):
            st.dataframe(display_df,hide_index=True)
            
    def graph_histogram(self, x, recipes_id):
        col = st.columns([1,3,1])
        with col[1]:
            fig, ax = plt.subplots(figsize=(10,6))
            sns.histplot(data=x, ax=ax)
            st.pyplot(fig)
            st.write(f"number of recipes : {len(x)}")
        display_df = self.dataframe[self.dataframe['id'].isin(recipes_id)]
        display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
        with st.expander("The 10 recipes with the most comments (with current filters)"):
            st.dataframe(display_df,hide_index=True)

    def display_graph(self):                        
        # Generate data
        print("début_display",self.delete)
        if self.delete ==False:
            
            with st.form(self.key):

                self.axis_x = self.__set_axis()
                self.range_axis_x = self.__set_range_axis()
                chosen_filters, range_filters = self.__filters(self.axis_x)
                x, recipes_id = self.get_data_points(self.dataframe, 
                                                        self.axis_x,
                                                        self.range_axis_x,
                                                        chosen_filters,
                                                        range_filters)
                y = range(len(x))

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    draw_graph_button = st.form_submit_button(label="Draw graph")
                with col2:
                    draw_boxplot_button = st.form_submit_button(label="Draw Box Plot")
                with col3:
                    draw_density_button = st.form_submit_button(label="Draw Density Plot")
                with col4:
                    draw_histogram_button = st.form_submit_button(label="Draw Histogram")
                with col5:
                    delete_graph_button = st.form_submit_button(label="Delete graph")
            
                if draw_graph_button:

                    self.graph_normal(x, recipes_id)
                    
                if draw_boxplot_button:

                    self.graph_boxplot(x, recipes_id)

                if draw_density_button  :

                    self.graph_density(x, recipes_id)

                if draw_histogram_button:
                        
                    self.graph_histogram(x, recipes_id)

                if delete_graph_button:
                    self.delete = True
                    print("delete",self.delete)
                    st.rerun()


class TimeStudy(Study):

    def __set_range_axis(self):
        range_axis_y = self.__create_slider_from_df(self.dataframe, self.axis_y)
        start_date = st.date_input("start date",self.dataframe["date"])
        end_date = st.date_input("start date",self.dataframe["date"])

        range_axis_x = (start_date, end_date)
        return range_axis_x, range_axis_y