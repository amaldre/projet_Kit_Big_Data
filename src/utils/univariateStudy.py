import streamlit as st
import math
import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter
import ast

logger = logging.getLogger(__name__)


class univariateStudy:

    def __init__(
        self,
        key,
        dataframe,
        plot_type,
        axis_x_list=None,
        filters=None,
        axis_x=None,
        name=None,
        default_values=None,
        log_axis_x=False,
        log_axis_y=False,
    ):
        # Attributs de la classe
        self.dataframe = dataframe
        self.axis_x_list = axis_x_list
        self.filters = filters
        self.axis_x = axis_x
        self.range_axis_x = None
        self.key = key
        self.delete = False
        self.plot_type = plot_type
        self.first_draw = True
        self.x = None
        self.y = None
        self.recipes_id = None
        self.name = key if name == None else name
        self.default_values = default_values
        self.default_values_save = default_values
        self.chosen_filters = None
        self.range_filters = None
        self.iteration = 1
        self.log_axis_x = log_axis_x
        self.log_axis_y = log_axis_y

    def __del__(self):
        return

    # Méthode d'affichage des attributs
    def print_self(self):
        print(self.axis_x_list, self.axis_x, self.range_axis_x, self.key)

    def save_graph(self):
        logger.info("Sauvegarde des attributs de l'objet Study avec key='%s'", self.key)
        range_filters = ""
        if self.chosen_filters != None:
            for i in range(len(self.chosen_filters)):
                range_filters += (
                    '"'
                    + str(self.chosen_filters[i])
                    + '":'
                    + str(self.range_filters[i])
                    + ", "
                )

        output = (
            f'axis_x="{self.axis_x}", plot_type="{self.plot_type}", \
                log_axis_x={self.log_axis_x}, log_axis_y={self.log_axis_y}, '
            + "default_values={"
            + f'"{self.axis_x}": {self.range_axis_x}, '
            + range_filters
            + f'"chosen_filters":{self.chosen_filters}'
            + "}"
        )

        st.write(output)

    def __set_axis(self):
        axis_x = st.selectbox(
            label="axis_x",
            options=self.axis_x_list,
            key=("axis_x" + self.key + str(self.iteration)),
        )
        logger.debug("Axes definis: axis_x=%s", axis_x)
        return axis_x

    def __create_slider_from_df(self, df, axis):

        min = math.floor(df[axis].min())
        max = math.ceil(df[axis].max())
        if self.default_values != None and axis in self.default_values:
            default_value = self.default_values[axis]

        else:
            default_value = [min, max]

        logger.debug(
            "Création d'un slider pour '%s' avec min=%d, max=%d", axis, min, max
        )
        return st.slider(
            label=f"Range for {axis}",
            min_value=min,
            max_value=max,
            value=default_value,
            step=1,
            key=(axis + self.key + str(self.iteration)),
        )

    def __set_date(self, axis):
        min_date = self.dataframe[axis].min()
        max_date = self.dataframe[axis].max()
        if self.default_values != None and axis in self.default_values:
            default_value = self.default_values[axis]
        else:
            default_value = [min_date, max_date]
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start date",
                value=default_value[0],
                min_value=min_date,
                max_value=max_date,
                key=("start date" + self.key + str(self.iteration)),
            )
        with col2:
            end_date = st.date_input(
                "End date",
                value=default_value[1],
                min_value=start_date,
                max_value=max_date,
                key=("end date" + self.key + str(self.iteration)),
            )
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return start_date, end_date

    def __set_number_ingredients(self, axis):
        if self.default_values != None and axis in self.default_values:
            default_value = self.default_values[axis]
        else:
            default_value = 10
        min, max = 1, 15
        logger.debug(
            "Creation d'un slider pour '%s' avec min=%d, max=%d", axis, min, max
        )
        return st.slider(
            label=f"Range for {axis}",
            min_value=min,
            max_value=max,
            value=default_value,
            step=1,
            key=(axis + self.key + str(self.iteration)),
        )

    def __set_range_axis(self, axis):
        if axis == "ingredients_replaced" or axis == "techniques":
            range_axis = self.__set_number_ingredients(axis)

        elif self.dataframe[axis].dtype == "datetime64[ns]":
            range_axis = self.__set_date(axis)
        else:
            range_axis = self.__create_slider_from_df(self.dataframe, axis)
        logger.debug(f"Plages definies pour axis {axis}: range_axis_x= {range_axis}")
        return range_axis

    def get_data_points(self, df, axis_x, range_axis_x, chosen_filters, range_filters):

        columns = [axis_x] + chosen_filters
        if "recipe_id" in self.dataframe.columns:
            columns += ["recipe_id"]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]

        if len(chosen_filters) > 0:
            for i, filter in enumerate(chosen_filters):
                df = df[
                    (df[filter] >= range_filters[i][0])
                    & (df[filter] <= range_filters[i][1])
                ]
        if self.default_values != None:
            self.default_values = {f"{self.axis_x}": self.range_axis_x}
            if self.range_filters != None:
                for i in range(len(self.range_filters)):
                    self.default_values[f"{self.chosen_filters[i]}"] = (
                        self.range_filters[i]
                    )
            self.default_values["chosen_filters"] = self.chosen_filters

        if "recipe_id" in self.dataframe.columns:
            return df[axis_x].values, df["recipe_id"].values
        else:
            return df[axis_x].values, None

    def get_data_points_ingredients(
        self, df, axis_x, range_axis_x, chosen_filters, range_filters
    ):
        columns = [axis_x] + chosen_filters
        if "recipe_id" in self.dataframe.columns:
            columns += ["recipe_id"]
        df = df[columns]
        # Apply filters
        if len(chosen_filters) > 0:
            for i, filter in enumerate(chosen_filters):
                df = df[
                    (df[filter] >= range_filters[i][0])
                    & (df[filter] <= range_filters[i][1])
                ]

        # Save axis and filters and their values
        if self.default_values != None:
            self.default_values = {f"{axis_x}": range_axis_x}
            if self.range_filters != None:
                for i in range(len(self.range_filters)):
                    self.default_values[f"{self.chosen_filters[i]}"] = (
                        self.range_filters[i]
                    )
            self.default_values["chosen_filters"] = self.chosen_filters

        # Calculates the numbers for each ingredients/techniques
        l_elts = list(df[axis_x])
        list_elts = []
        for item in l_elts:
            for i in item:
                list_elts.append(i)
        element_counts_elts = Counter(list_elts)
        top_elts = element_counts_elts.most_common(range_axis_x)
        list_elts = []
        for i in range(len(top_elts)):
            list_elts.append(top_elts[i][0])
        count_elts = []
        for elt in list_elts:
            count_elts.append(element_counts_elts[elt])

        if "recipe_id" in self.dataframe.columns:
            return list_elts, count_elts, df["recipe_id"].values
        else:
            return list_elts, count_elts, None

    def __filters(self, axis_x):
        if self.default_values != None:
            default_values = self.default_values["chosen_filters"]
        else:
            default_values = None
        filters = [filtre for filtre in self.filters if (filtre != axis_x)]
        chosen_filters = st.multiselect(
            label="filters",
            default=default_values,
            options=filters,
            key=("filters" + self.key + str(self.iteration)),
        )
        range_filters = []
        for filter in chosen_filters:
            range_axis = self.__set_range_axis(filter)
            range_filters.append(range_axis)
        logger.debug("Filtres choisis : %s", chosen_filters)

        return chosen_filters, range_filters

    # Pour les differents types de graphes
    def graph_normal(self, x):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, range(len(x)), marker="o", linewidth=0.7, markersize=0.5)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes : {len(x)}")

    def graph_boxplot(self, x):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=x, ax=ax, orient="h")
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")

    def graph_density(self, x):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data=x, ax=ax, linewidth=2)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")

    def graph_histogram(self, x):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=x, ax=ax, bins=25)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")

    def graph_bar_elts(self, nb_elts_display, count_elts):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=nb_elts_display, y=count_elts)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {sum(count_elts)}")

    def __draw_graph(self, x, y, recipes_id):
        col = st.columns([1, 3, 1])
        with col[1]:
            if self.plot_type == "boxplot":
                self.graph_boxplot(x)
            elif self.plot_type == "density":
                self.graph_density(x)
            elif self.plot_type == "histogram":
                self.graph_histogram(x)
            elif (
                self.plot_type == "bar_ingredients"
                or self.plot_type == "bar_techniques"
            ):
                self.graph_bar_elts(x, y)
        display_df = self.dataframe[self.dataframe["recipe_id"].isin(recipes_id)]
        display_df = display_df.sort_values(by="comment_count", ascending=False)[:10]
        with st.expander(
            "The 10 recipes with the most comments (with current filters)"
        ):
            st.dataframe(display_df, hide_index=True)

    def axis_graph(self, fig, ax):
        ax.set_title(self.name)
        if self.log_axis_x:
            ax.set_xlabel("log " + self.axis_x)
            ax.set_xscale("log")
        else:
            ax.set_xlabel(self.axis_x)

        if self.log_axis_y:
            ax.set_ylabel("log " + "number of recipes")
            ax.set_yscale("log")
        else:
            ax.set_ylabel("number of recipes")
        ax.grid(True, which="both", linestyle="-", linewidth=0.7, alpha=0.7)
        st.pyplot(fig, clear_figure=True)

    def display_graph(self, free=False, explanation=None):
        self.default_values = self.default_values_save
        logger.info("Affichage du graphique pour l'instance avec key='%s'", self.key)
        chosen_filters = []
        range_filters = []
        if self.delete == False:
            with st.container(border=True):
                st.markdown(f"**{self.name}**")
                graph_container = st.empty()
                with graph_container.expander("**filters**", expanded=free):
                    if free == True:
                        axis_x = self.__set_axis()
                    else:
                        axis_x = self.axis_x
                    self.range_axis_x = self.__set_range_axis(axis_x)
                    if self.filters != None and len(self.filters) > 0:
                        st.write("extra_filters")
                        chosen_filters, range_filters = self.__filters(axis_x)
                        self.chosen_filters = chosen_filters
                        self.range_filters = range_filters

                    with st.form(self.key, border=False):
                        pos = 0
                        col = st.columns(2)
                        with col[pos]:
                            if np.issubdtype(self.dataframe[axis_x].dtype, np.number):
                                self.log_axis_x = st.checkbox(
                                    "log axis_x",
                                    key=("log axis_x" + self.key + str(self.iteration)),
                                    value=self.log_axis_x,
                                )
                                pos += 1
                            else:
                                self.log_axis_x = False
                        with col[pos]:
                            self.log_axis_y = st.checkbox(
                                "log axis_y",
                                key=("log axis_y" + self.key + str(self.iteration)),
                                value=self.log_axis_x,
                            )
                        if axis_x == "ingredients_replaced":
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button(label="Draw Bar"):
                                    self.axis_x = axis_x
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points_ingredients(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )
                                    self.plot_type = "bar_ingredients"

                            with col2:
                                if st.form_submit_button(label="Delete graph"):
                                    self.delete = True
                                    st.rerun()

                        elif axis_x == "techniques":
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button(label="Draw Bar"):
                                    self.axis_x = axis_x
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points_ingredients(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )
                                    self.plot_type = "bar_techniques"

                            with col2:
                                if st.form_submit_button(label="Delete graph"):
                                    self.delete = True
                                    st.rerun()

                        else:
                            if free == True:
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    if st.form_submit_button(label="Draw Box Plot"):
                                        self.axis_x = axis_x
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                        self.plot_type = "boxplot"

                                with col2:
                                    if st.form_submit_button(label="Draw Density Plot"):
                                        self.axis_x = axis_x
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                        self.plot_type = "density"

                                with col3:
                                    if st.form_submit_button(label="Draw Histogram"):
                                        self.axis_x = axis_x
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                        self.plot_type = "histogram"

                                col1, col2, _ = st.columns(3)
                                with col1:
                                    if st.form_submit_button(label="Save graph"):
                                        self.save_graph()

                                with col2:
                                    if st.form_submit_button(label="Delete graph"):
                                        self.delete = True
                                        print("delete", self.delete)
                                        st.rerun()

                            else:
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button(label="Draw graph"):
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )

                                with col2:
                                    if st.form_submit_button(label="Reset graph"):
                                        self.axis_x = axis_x
                                        self.default_values = self.default_values_save
                                        print(self.default_values)
                                        range_filters_save = [
                                            self.default_values_save[filter]
                                            for filter in self.default_values_save[
                                                "chosen_filters"
                                            ]
                                        ]
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.default_values_save[self.axis_x],
                                            self.default_values_save["chosen_filters"],
                                            range_filters_save,
                                        )
                                        self.iteration += 1
                                        graph_container.empty()
                                        st.rerun()

                if self.first_draw == True:
                    self.axis_x = axis_x
                    self.x, self.recipes_id = self.get_data_points(
                        self.dataframe,
                        self.axis_x,
                        self.range_axis_x,
                        chosen_filters,
                        range_filters,
                    )
                    self.first_draw = False

                self.__draw_graph(self.x, self.y, self.recipes_id)
                if explanation != None:
                    st.write(explanation)
