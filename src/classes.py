import streamlit as st
import math
import matplotlib.pyplot as plt

class Study:

    def __init__(self, dataframe, axis_x_list, axis_y_list, filters, key):
        # Attributs de la classe
        self.dataframe = dataframe
        self.axis_x_list = axis_x_list
        self.axis_y_list = axis_y_list
        self.filters = filters
        self.axis_x = None
        self.axis_y = None
        self.range_axis_x = None
        self.range_axis_y = None
        self.key = key
        self.delete = False

    def __del__(self):
        return

    # Méthode d'affichage des attributs
    def print_self(self):
        print(
            self.axis_x_list,
            self.axis_y_list,
            self.axis_x,
            self.axis_y,
            self.range_axis_x,
            self.range_axis_y,
            self.key)


    def __set_axis(self):
        axis_y = st.selectbox(label="axis_y", options = self.axis_y_list)
        axis_x = st.selectbox(label="axis_x", options = self.axis_x_list)
        return axis_x, axis_y
    
    def __create_slider_from_df(self, df,column):
        min = math.floor(df[column].min())
        max = math.ceil(df[column].max())
        return st.slider(label = f"range for {column}", min_value=min, max_value=max, value=(min,max), step=1)

    def get_data_points(self, df, axis_x, axis_y, range_axis_x, range_axis_y, chosen_filters, range_filters):
        columns = [axis_x,axis_y,"id"] + [filtre for filtre in chosen_filters if (filtre != axis_x and filtre != axis_y)]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]
        df = df[(df[axis_y] >= range_axis_y[0]) & (df[axis_y] <= range_axis_y[1])]
        if len(chosen_filters)>0:
            for i,filter in enumerate(chosen_filters):
                df = df[(df[filter] >= range_filters[i][0]) & (df[filter] <= range_filters[i][1])]
        return df[axis_x].values, df[axis_y].values, df["id"].values
    

    def __set_range_axis(self):
        range_axis_y = self.__create_slider_from_df(self.dataframe, self.axis_y)
        range_axis_x = self.__create_slider_from_df(self.dataframe, self.axis_x)
        return range_axis_x, range_axis_y

    def __filters(self, axis_x, axis_y):
        filters = [filtre for filtre in self.filters if (filtre != axis_x and filtre != axis_y)]
        chosen_filters = st.sidebar.multiselect(label ="filters", options=filters)
        print(chosen_filters)
        range_filters = []
        for filter in chosen_filters:
            min = math.floor(self.dataframe[filter].min())
            max = math.ceil(self.dataframe[filter].max())
            range = st.sidebar.slider(filter, min_value=min, max_value=max, value=(min,max))
            print(range)
            range_filters.append(range)
            print(range_filters)
        print(range_filters)
        return chosen_filters,range_filters

    def display_graph(self):
        # Generate data
        print("début_display",self.delete)
        if self.delete ==False:
            
            with st.form(self.key):

                self.axis_x, self.axis_y = self.__set_axis()
                self.range_axis_x, self.range_axis_y = self.__set_range_axis()
                chosen_filters, range_filters = self.__filters(self.axis_x, self.axis_y)
                x, y, recipes_id = self.get_data_points(self.dataframe, 
                                                        self.axis_x, 
                                                        self.axis_y, 
                                                        self.range_axis_x, 
                                                        self.range_axis_y, 
                                                        chosen_filters,
                                                        range_filters)
            
                if st.form_submit_button(label="Draw graph"):

                    col = st.columns([1,3,1])

                    with col[1]:
                    # Create a figure
                        fig, ax = plt.subplots(figsize=(10,6))
                        ax.scatter(x, y, s=0.5)
                        # Display Matplotlib figure in Streamlit
                        st.pyplot(fig)
                        st.write(f"number of recipes : {len(x)}")

                    display_df = self.dataframe[self.dataframe['id'].isin(recipes_id)]
                    display_df = display_df.sort_values(by="count_total",ascending=False)[:10]
                    with st.expander("The 10 recipes with the most comments (with current filters)"):
                        st.dataframe(display_df,hide_index=True)
                    
                if st.form_submit_button(label="Delete graph"):
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