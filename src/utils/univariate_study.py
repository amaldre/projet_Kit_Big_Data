""" 
Module de classe pour l'analyse univariée et la visualisation des données d'un dataframe.
"""

import math
import logging
from collections import Counter

import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from utils.base_study import base_study

logger = logging.getLogger(__name__)


class univariate_study(base_study):
    """
    A class to perform univariate data analysis and visualization on a dataframe.
    Supports filtering, axis transformations, and multiple plot types.
    """

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
        self.name = key if name is None else name
        self.default_values = default_values
        self.default_values_save = default_values
        self.chosen_filters = None
        self.range_filters = None
        self.iteration = 1
        self.log_axis_x = log_axis_x
        self.log_axis_y = log_axis_y

    def __del__(self):
        # No special cleanup required
        return

    def print_self(self):
        """
        Print current object attributes for debugging.
        """
        print(self.axis_x_list, self.axis_x, self.range_axis_x, self.key)

    def save_graph(self):
        """
        Save the graph configuration to Streamlit output.
        """
        logger.info("Saving object attributes with key='%s'", self.key)
        range_filters_str = ""
        if self.chosen_filters is not None:
            for i, chosen_filter in enumerate(self.chosen_filters):
                range_filters_str += f'"{chosen_filter}":{self.range_filters[i]}, '

        output = (
            f'axis_x="{self.axis_x}", plot_type="{self.plot_type}", '
            f"log_axis_x={self.log_axis_x}, log_axis_y={self.log_axis_y}, "
            + "default_values={"
            + f'"{self.axis_x}": {self.range_axis_x}, '
            + range_filters_str
            + f'"chosen_filters":{self.chosen_filters}'
            + "}"
        )
        st.write(output)

    def __set_axis(self):
        """
        Display a select box to choose the axis_x variable.
        """
        axis_x = st.selectbox(
            label="axis_x",
            options=self.axis_x_list,
            key=("axis_x" + self.key + str(self.iteration)),
        )
        logger.debug("Axes defined: axis_x=%s", axis_x)
        return axis_x

    def __set_number_ingredients(self, axis):
        """
        Create a slider for selecting the number of ingredients or techniques to display.
        """
        if self.default_values is not None and axis in self.default_values:
            default_value = self.default_values[axis]
        else:
            default_value = 10

        min_val, max_val = 1, 15
        logger.debug(
            "Creating a slider for '%s' with min=%d, max=%d", axis, min_val, max_val
        )
        return st.slider(
            label=f"Range for {axis}",
            min_value=min_val,
            max_value=max_val,
            value=default_value,
            step=1,
            key=(axis + self.key + str(self.iteration)),
        )

    def __set_range_axis(self, axis):
        """
        Determine the appropriate input widget (slider/date input) based on column type.
        """
        if axis in ("ingredients_replaced", "techniques"):
            range_axis = self.__set_number_ingredients(axis)
        elif self.dataframe[axis].dtype == "datetime64[ns]":
            range_axis = self._base_study__set_date(axis)
        else:
            range_axis = self._base_study__create_slider_from_df(self.dataframe, axis)
        logger.debug("Range defined for axis %s: range_axis_x=%s", axis, range_axis)
        return range_axis

    def get_data_points(self, df, axis_x, range_axis_x, chosen_filters, range_filters):
        """
        Extract data points for the selected axis and filters.
        """
        columns = [axis_x] + chosen_filters
        if "recipe_id" in self.dataframe.columns:
            columns += ["recipe_id"]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]

        if chosen_filters:
            for i, chosen_filter in enumerate(chosen_filters):
                df = df[
                    (df[chosen_filter] >= range_filters[i][0])
                    & (df[chosen_filter] <= range_filters[i][1])
                ]

        if self.default_values is not None:
            self.default_values = {f"{self.axis_x}": self.range_axis_x}
            if self.range_filters is not None:
                for i, chosen_filter in enumerate(self.chosen_filters):
                    self.default_values[f"{chosen_filter}"] = self.range_filters[i]
            self.default_values["chosen_filters"] = self.chosen_filters

        if "recipe_id" in self.dataframe.columns:
            return df[axis_x].values, df["recipe_id"].values
        return df[axis_x].values, None

    def get_data_points_ingredients(
        self, df, axis_x, range_axis_x, chosen_filters, range_filters
    ):
        """
        Extract and count data points for ingredients or techniques.
        """
        columns = [axis_x] + chosen_filters
        if "recipe_id" in self.dataframe.columns:
            columns += ["recipe_id"]
        df = df[columns]

        # Apply filters
        if chosen_filters:
            for i, chosen_filter in enumerate(chosen_filters):
                df = df[
                    (df[chosen_filter] >= range_filters[i][0])
                    & (df[chosen_filter] <= range_filters[i][1])
                ]

        # Save axis and filters
        if self.default_values is not None:
            self.default_values = {f"{axis_x}": range_axis_x}
            if self.range_filters is not None:
                for i, chosen_filter in enumerate(self.chosen_filters):
                    self.default_values[f"{chosen_filter}"] = self.range_filters[i]
            self.default_values["chosen_filters"] = self.chosen_filters

        # Count top elements
        elements_list = []
        for item_list in df[axis_x]:
            elements_list.extend(item_list)

        element_counts = Counter(elements_list)
        top_elements = element_counts.most_common(range_axis_x)
        nb_elts_display = [element[0] for element in top_elements]
        count_elts = [element_counts[elt] for elt in nb_elts_display]

        if "recipe_id" in self.dataframe.columns:
            return nb_elts_display, count_elts, df["recipe_id"].values
        return nb_elts_display, count_elts, None

    def __filters(self, axis_x):
        """
        Display and handle filter selection widgets.
        """
        if self.default_values is not None:
            default_values = self.default_values["chosen_filters"]
        else:
            default_values = None

        all_filters = [f for f in self.filters if f != axis_x]
        chosen_filters = st.multiselect(
            label="filters",
            default=default_values,
            options=all_filters,
            key=("filters" + self.key + str(self.iteration)),
        )
        range_filters = []
        for chosen_filter in chosen_filters:
            range_axis = self.__set_range_axis(chosen_filter)
            range_filters.append(range_axis)
        logger.debug("Selected filters: %s", chosen_filters)
        return chosen_filters, range_filters

    def graph_boxplot(self, x):
        """
        Draw a boxplot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=x, ax=ax, orient="h")
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")
        return True

    def graph_density(self, x):
        """
        Draw a density (KDE) plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data=x, ax=ax, linewidth=2)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")
        return True

    def graph_histogram(self, x):
        """
        Draw a histogram plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=x, ax=ax, bins=25)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {len(x)}")
        return True

    def graph_bar_elts(self, nb_elts_display, count_elts):
        """
        Draw a bar plot for ingredients or techniques.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=nb_elts_display, y=count_elts)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"number of recipes in the graph: {sum(count_elts)}")
        return True

    def __draw_graph(self, x, y, recipes_id):
        """
        Display the selected graph type and related data.
        """
        col = st.columns([1, 3, 1])
        with col[1]:
            if self.plot_type == "boxplot":
                self.graph_boxplot(x)
            elif self.plot_type == "density":
                self.graph_density(x)
            elif self.plot_type == "histogram":
                self.graph_histogram(x)
            elif self.plot_type in ("bar_ingredients", "bar_techniques"):
                self.graph_bar_elts(x, y)

        if recipes_id is not None:
            display_df = self.dataframe[self.dataframe["recipe_id"].isin(recipes_id)]
            display_df = display_df.sort_values(by="comment_count", ascending=False)[
                :10
            ]
            with st.expander(
                "The 10 recipes with the most comments (with current filters)"
            ):
                st.dataframe(display_df, hide_index=True)
        return True

    def axis_graph(self, fig, ax):
        """
        Set axis labels, scale, and grid for the plot.
        """
        ax.set_title(self.name)
        if self.log_axis_x:
            ax.set_xlabel("log " + self.axis_x)
            ax.set_xscale("log")
        else:
            ax.set_xlabel(self.axis_x)

        if self.log_axis_y:
            ax.set_ylabel("log number of recipes")
            ax.set_yscale("log")
        else:
            ax.set_ylabel("number of recipes")

        ax.grid(True, which="both", linestyle="-", linewidth=0.7, alpha=0.7)
        st.pyplot(fig, clear_figure=True)
        return True

    def display_graph(self, free=False, explanation=None):
        """
        Main method to display the graph and handle interaction with the filters and controls.
        """
        self.default_values = self.default_values_save
        logger.info("Displaying graph for instance with key='%s'", self.key)
        chosen_filters = []
        range_filters = []
        if not self.delete:
            with st.container():
                st.markdown(f"**{self.name}**")
                graph_container = st.empty()
                with graph_container.expander("**filters**", expanded=free):
                    if free:
                        axis_x = self.__set_axis()
                    else:
                        axis_x = self.axis_x
                    self.range_axis_x = self.__set_range_axis(axis_x)

                    if self.filters is not None and self.filters:
                        st.write("extra_filters")
                        chosen_filters, range_filters = self.__filters(axis_x)
                        self.chosen_filters = chosen_filters
                        self.range_filters = range_filters

                    with st.form(self.key):
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
                                value=self.log_axis_y,
                            )

                        if axis_x in ("ingredients_replaced", "techniques"):
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
                                    if axis_x == "ingredients_replaced":
                                        self.plot_type = "bar_ingredients"
                                    else:
                                        self.plot_type = "bar_techniques"

                            with col2:
                                if st.form_submit_button(label="Delete graph"):
                                    self.delete = True
                                    st.experimental_rerun()

                        else:
                            if free:
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
                                        st.experimental_rerun()

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
                                        range_filters_save = [
                                            self.default_values_save[filt]
                                            for filt in self.default_values_save[
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
                                        st.experimental_rerun()

                if self.first_draw:
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
                if explanation is not None:
                    st.write(explanation)
                return True
