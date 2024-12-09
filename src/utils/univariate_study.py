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
from src.utils.base_study import BaseStudy

logger = logging.getLogger(__name__)


class UnivariateStudy(BaseStudy):
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
        graph_pad=10,
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
        self.graph_pad = graph_pad

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
            f'axis_x="{self.axis_x}", filters={self.chosen_filters}, plot_type="{self.plot_type}", \
                log_axis_x={self.log_axis_x}, log_axis_y={self.log_axis_y}, '
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
        Creates a slider for selecting the number of ingredients or techniques to display.

        :param axis: axis to create the slider for
        :type axis: str
        :return: slider widget
        :rtype: streamlit.slider
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
            label=f"Plage de valeurs pour : {axis}",
            min_value=min_val,
            max_value=max_val,
            value=default_value,
            step=1,
            key=(axis + self.key + str(self.iteration)),
        )

    def __set_range_axis(self, axis):
        """
        Determine the appropriate input widget (slider/date input) based on column type.

        :param axis: axis to create the range for
        :type axis: str
        :return: range widget
        :rtype: streamlit.slider or streamlit.date_input
        """
        if axis in ("Ingrédients", "Techniques utilisées"):
            range_axis = self.__set_number_ingredients(axis)
        elif self.dataframe[axis].dtype == "datetime64[ns]":
            range_axis = self._BaseStudy__set_date(axis)
        else:
            range_axis = self._BaseStudy__create_slider_from_df(self.dataframe, axis)
        logger.debug("Range defined for axis %s: range_axis_x=%s", axis, range_axis)
        return range_axis

    def get_data_points(self, df, axis_x, range_axis_x, chosen_filters, range_filters):
        """
        Extract data points for the selected axis and filters.

        :param df: dataframe to extract data from
        :type df: pandas.DataFrame
        :param axis_x: axis x
        :type axis_x: str
        :param range_axis_x: range for axis x
        :type range_axis_x: tuple
        :param chosen_filters: filters to apply
        :type chosen_filters: list
        :param range_filters: range for filters
        :type range_filters: list
        :return: data points for axis x and recipe_id
        :rtype: tuple
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

        :param df: dataframe to extract data from
        :type df: pandas.DataFrame
        :param axis_x: axis x
        :type axis_x: str
        :param range_axis_x: range for axis x
        :type range_axis_x: tuple
        :param chosen_filters: filters to apply
        :type chosen_filters: list
        :param range_filters: range for filters
        :type range_filters: list
        :return: data points for axis x, count of elements, and recipe_id
        :rtype: tuple
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

        :param axis_x: axis x
        :type axis_x: str
        :return: selected filters and their ranges
        :rtype: tuple
        """
        if self.default_values is not None:
            default_values = self.default_values["chosen_filters"]
        else:
            default_values = None

        all_filters = [f for f in self.filters if f != axis_x]
        chosen_filters = st.multiselect(
            label="Filtres",
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

        :param x: data points for the boxplot
        :type x: list
        :return: True if the plot was drawn successfully
        :rtype: bool
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=x, ax=ax, orient="h")
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"Nombre de recettes prises en compte dans le graphe : {len(x)}")
        return True

    def graph_density(self, x):
        """
        Draw a density (KDE) plot.

        :param x: data points for the density plot
        :type x: list
        :return: plot object
        :rtype: matplotlib.pyplot.Figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data=x, ax=ax, linewidth=2)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"Nombre de recettes prises en compte dans le graphe : {len(x)}")
        return True

    def graph_histogram(self, x):
        """
        Draw a histogram plot.

        :param x: data points for the histogram
        :type x: list
        :return: plot object
        :rtype: matplotlib.pyplot.Figure
        """

        if self.axis_x == "Date de publication de la recette" and isinstance(
            self.range_axis_x[1], pd.Timestamp
        ):
            nb_bin = self.range_axis_x[1].year - self.range_axis_x[0].year
        else:
            nb_bin = 25

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=x, ax=ax, bins=nb_bin)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"Nombre de recettes affichées dans le graphe : {len(x)}")
        return True

    def graph_bar_elts(self, nb_elts_display, count_elts):
        """
        Draw a bar plot for ingredients or techniques.

        :param nb_elts_display: elements to display
        :type nb_elts_display: list
        :param count_elts: count of elements
        :type count_elts: list
        :return: plot object
        :rtype: matplotlib.pyplot.Figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=nb_elts_display, y=count_elts)
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        self.axis_graph(fig, ax)
        st.write(f"Nombre d'éléments affichées dans le graphe : {sum(count_elts)}")
        return True

    def __draw_graph(self, x, y, recipes_id):
        """
        Display the selected graph type and related data.

        :param x: abscissa data points
        :type x: list
        :param y: ordinate data points
        :type y: list
        :param recipes_id: list of recipe ids
        :type recipes_id: list
        :return: plot object
        :rtype: matplotlib.pyplot.Figure
        """
        col = st.columns([self.graph_pad, 30, self.graph_pad])
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
            display_df = display_df.sort_values(
                by="Nombre de commentaires", ascending=False
            )[:10]
            with st.expander(
                "Recettes avec le plus de commentaires (avec les filtres actuels)"
            ):
                st.dataframe(display_df, hide_index=True)
        return True

    def axis_graph(self, fig, ax):
        """
        Set axis labels, scale, and grid for the plot.

        :param fig: figure object
        :type fig: matplotlib.pyplot.Figure
        :param ax: axis object
        :type ax: matplotlib.pyplot.Axes
        :return: plot object
        :rtype: matplotlib.pyplot.Figure
        """
        ax.set_title(self.name, fontsize=16, pad=20, weight="bold")
        ax.set_xlabel(self.axis_x, fontsize=16)
        ax.set_ylabel("Nombre de recettes", fontsize=16)
        if self.log_axis_x:
            ax.set_xscale("log")
        if self.log_axis_y:
            ax.set_yscale("log")
        ax.grid(True, which="both", linestyle="-", linewidth=0.7, alpha=0.4)
        st.pyplot(fig, clear_figure=True)
        return True

    def display_graph(self, free=False, explanation=None):
        """
        Main method to display the graph and handle interaction with the filters and controls.

        :param free: condition pour choisir les axes et les filtres additionnels, defaults to False
        :type free: bool, optional
        :param explanation: explication du graphique, defaults to None
        :type explanation: str, optional
        :return: True if the plot was drawn successfully
        :rtype: bool
        """
        self.default_values = self.default_values_save
        logger.info("Displaying graph for instance with key='%s'", self.key)
        chosen_filters = []
        range_filters = []
        if not self.delete:
            with st.container(border=True):
                st.markdown(f"**{self.name}**")
                graph_container = st.empty()
                with graph_container.expander("**Filtres**", expanded=free):
                    if free:
                        axis_x = self.__set_axis()
                    else:
                        axis_x = self.axis_x
                    self.range_axis_x = self.__set_range_axis(axis_x)

                    if self.filters is not None and self.filters:
                        st.write("Filtres additionnels")
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
                                value=self.log_axis_y,
                            )

                        if axis_x in ("Ingrédients", "Techniques utilisées"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.form_submit_button(
                                    label="Tracer un diagramme en barre"
                                ):
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
                                    if axis_x == "Ingrédients":
                                        self.plot_type = "bar_ingredients"
                                    else:
                                        self.plot_type = "bar_techniques"

                            if free:
                                with col2:
                                    if st.form_submit_button(
                                        label="Supprimer le graphe"
                                    ):
                                        self.delete = True
                                        st.experimental_rerun()
                                with col3:
                                    if st.form_submit_button(
                                        label="Paramètres du graphe"
                                    ):
                                        self.save_graph()
                            else:
                                with col2:
                                    if st.form_submit_button(
                                        label="Réinitialiser le graphe"
                                    ):
                                        self.axis_x = axis_x
                                        self.default_values = self.default_values_save
                                        range_filters_save = [
                                            self.default_values_save[filters]
                                            for filters in self.default_values_save[
                                                "chosen_filters"
                                            ]
                                        ]
                                        self.x, self.recipes_id = (
                                            self.get_data_points_ingredients(
                                                self.dataframe,
                                                self.axis_x,
                                                self.default_values_save[self.axis_x],
                                                self.default_values_save[
                                                    "chosen_filters"
                                                ],
                                                range_filters_save,
                                            )
                                        )
                                        self.iteration += 1
                                        graph_container.empty()
                                        st.rerun()

                        else:
                            if free:
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    if st.form_submit_button(
                                        label="Tracer un graphe box plot"
                                    ):
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
                                    if st.form_submit_button(
                                        label="Tracer un graphe de densité"
                                    ):
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
                                    if st.form_submit_button(
                                        label="Tracer un histogramme"
                                    ):
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
                                    if st.form_submit_button(
                                        label="Paramètres du graphe"
                                    ):
                                        self.save_graph()

                                with col2:
                                    if st.form_submit_button(
                                        label="Supprimer le graphe"
                                    ):
                                        self.delete = True
                                        st.rerun()

                            else:
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button(label="Trace le graphe"):
                                        self.x, self.recipes_id = self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.range_axis_x,
                                            chosen_filters,
                                            range_filters,
                                        )
                                with col2:
                                    if st.form_submit_button(
                                        label="Réinitialiser le graphe"
                                    ):
                                        self.axis_x = axis_x
                                        self.default_values = self.default_values_save
                                        range_filters_save = [
                                            self.default_values_save["filters"]
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
                                        st.rerun()

                if self.first_draw:
                    self.axis_x = axis_x
                    if self.axis_x in ("Ingrédients", "Techniques utilisées"):
                        self.x, self.y, self.recipes_id = (
                            self.get_data_points_ingredients(
                                self.dataframe,
                                self.axis_x,
                                self.range_axis_x,
                                chosen_filters,
                                range_filters,
                            )
                        )
                    else:
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
