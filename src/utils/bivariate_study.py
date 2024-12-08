""" 
Module de classe pour l'analyse bivariée.
"""

import streamlit as st
import math
import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from utils.base_study import BaseStudy


# Créez un logger spécifique pour ce module
logger = logging.getLogger(__name__)


class BivariateStudy(BaseStudy):
    """
    Classe pour l'analyse bivariée.

    :param BaseStudy: Classe parente
    :type BaseStudy: Class
    """

    def __init__(
        self,
        key,
        dataframe,
        plot_type,
        axis_x_list=None,
        axis_y_list=None,
        filters=None,
        axis_x=None,
        axis_y=None,
        name=None,
        default_values=None,
        log_axis_x=False,
        log_axis_y=False,
        graph_pad=10,
    ):
        # Attributs de la classe
        self.dataframe = dataframe
        self.axis_x_list = axis_x_list
        self.axis_y_list = axis_y_list
        self.filters = filters
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.range_axis_x = None
        self.range_axis_y = None
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

        # Log l'initialisation de l'objet
        logger.info("Instance de Study creee avec key='%s'", self.key)

    def __del__(self):
        logger.info("Instance de Study avec key='%s' supprimee", self.key)
        return

    # Méthode d'affichage des attributs
    def save_graph(self):
        """
        Méthode pour sauvegarder les attributs du graphe.

        :return: True si la sauvegarde a réussi
        :rtype: bool
        """
        logger.info("Sauvegarde des attributs de l'objet Study avec key='%s'", self.key)
        range_filters = ""
        if self.chosen_filters is not None:
            for i in range(len(self.chosen_filters)):
                range_filters += (
                    '"'
                    + str(self.chosen_filters[i])
                    + '":'
                    + str(self.range_filters[i])
                    + ", "
                )

        output = (
            f'axis_x="{self.axis_x}", axis_y="{self.axis_y}", filters={self.chosen_filters}, plot_type="{self.plot_type}", \
                log_axis_x={self.log_axis_x}, log_axis_y={self.log_axis_y}, '
            + "default_values={"
            + f'"{self.axis_x}": {self.range_axis_x}, \
                "{self.axis_y}": {self.range_axis_y}, '
            + range_filters
            + f'"chosen_filters":{self.chosen_filters}'
            + "}"
        )

        st.write(output)
        return True

    def __set_axis(self):
        """
        Méthode pour définir les axes du graphique.

        :return: Les axes du graphique
        :rtype: tuple
        """
        axis_x = st.selectbox(
            label="axis_x",
            options=self.axis_x_list,
            key=("axis_x" + self.key + str(self.iteration)),
        )
        axis_y = st.selectbox(
            label="axis_y",
            options=[axis for axis in self.axis_y_list if axis != axis_x],
            key=("axis_y" + self.key + str(self.iteration)),
        )

        logger.debug("Axes definis: axis_x=%s, axis_y=%s", axis_x, axis_y)
        return axis_x, axis_y

    def get_data_points(
        self,
        df,
        axis_x,
        axis_y,
        range_axis_x,
        range_axis_y,
        chosen_filters,
        range_filters,
    ):
        """
        Méthode pour obtenir les points de données pour le graphique.

        :param df: dataframe
        :type df: pandas.DataFrame
        :param axis_x: axe x
        :type axis_x: str
        :param axis_y: axe y
        :type axis_y: str
        :param range_axis_x: plage de l'axe x
        :type range_axis_x: tuple
        :param range_axis_y: plage de l'axe y
        :type range_axis_y: tuple
        :param chosen_filters: filtres choisis
        :type chosen_filters: list
        :param range_filters: plages des filtres
        :type range_filters: list
        :return: Les points de données pour le graphique
        :rtype: tuple
        """
        columns = [axis_x, axis_y] + chosen_filters
        if "recipe_id" in self.dataframe.columns:
            columns += ["recipe_id"]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]
        df = df[(df[axis_y] >= range_axis_y[0]) & (df[axis_y] <= range_axis_y[1])]
        if len(chosen_filters) > 0:
            for i, filter in enumerate(chosen_filters):
                df = df[
                    (df[filter] >= range_filters[i][0])
                    & (df[filter] <= range_filters[i][1])
                ]
        if self.default_values is not None:
            self.default_values = {
                f"{self.axis_x}": self.range_axis_x,
                f"{self.axis_y}": self.range_axis_y,
            }
            if self.range_filters is not None:
                for i in range(len(self.range_filters)):
                    self.default_values[f"{self.chosen_filters[i]}"] = (
                        self.range_filters[i]
                    )
            self.default_values["chosen_filters"] = self.chosen_filters

        if "recipe_id" in self.dataframe.columns:
            return df[axis_x].values, df[axis_y].values, df["recipe_id"].values
        else:
            return df[axis_x].values, df[axis_y].values, None

    def __set_range_axis(self, axis):
        """
        Méthode pour définir la plage de l'axe.

        :param axis: axe
        :type axis: str
        :return: plage de l'axe
        :rtype: tuple
        """

        if self.dataframe[axis].dtype == "datetime64[ns]":
            range_axis = self._BaseStudy__set_date(axis)
        else:
            range_axis = self._BaseStudy__create_slider_from_df(self.dataframe, axis)
        logger.debug(f"Plages definies pour axis {axis}: range_axis_x= {range_axis}")
        return range_axis

    def __filters(self, axis_x, axis_y):
        """
        Méthode pour définir les filtres.

        :param axis_x: axe x
        :type axis_x: str
        :param axis_y: axe y
        :type axis_y: str
        :return: Les filtres choisis et leurs plages
        :rtype: tuple
        """
        if self.default_values is not None:
            default_values = self.default_values["chosen_filters"]
        else:
            default_values = None
        filters = [
            filtre for filtre in self.filters if (filtre != axis_x and filtre != axis_y)
        ]
        chosen_filters = st.multiselect(
            label="Filtres",
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

    def __draw_plot(self, x, y, recipes_id):
        """
        Méthode pour dessiner le graphique.

        :param x: abscisse des points
        :type x: list
        :param y: ordonnée des points
        :type y: list
        :param recipes_id: id des recettes
        :type recipes_id: list
        :return: True si le dessin a réussi
        :rtype: bool
        """
        col = st.columns([self.graph_pad, 30, self.graph_pad])
        with col[1]:

            fig, ax = plt.subplots(figsize=(10, 6))

            ax.set_title(self.name, fontsize=16, pad=20, weight="bold")
            if self.plot_type != "density map":
                ax.set_xlabel(self.axis_x, fontsize=16)
                ax.set_ylabel(self.axis_y, fontsize=16)
                if self.log_axis_x:
                    ax.set_xscale("log")
                if self.log_axis_y:
                    ax.set_yscale("log")

            else:
                if self.log_axis_x:
                    ax.set_xlabel("log " + self.axis_x, fontsize=16)
                    x = np.log(x)
                else:
                    ax.set_xlabel(self.axis_x, fontsize=16)
                if self.log_axis_y:
                    ax.set_ylabel("log " + self.axis_y, fontsize=16)
                    y = np.log(y)
                else:
                    ax.set_ylabel(self.axis_y, fontsize=16)

            if self.plot_type == "scatter":
                ax.scatter(x, y, s=1)
            elif self.plot_type == "plot":
                ax.plot(x, y)
            elif self.plot_type == "density map":
                if self.axis_x == "Date de publication de la recette":
                    x = x.astype(np.int64) // 10**9
                    ax.set_xticks(np.linspace(min(x), max(x), 7))
                    ax.set_xticklabels(
                        pd.to_datetime(
                            np.linspace(min(x), max(x), 7), unit="s"
                        ).strftime("%Y")
                    )
                hb = ax.hexbin(
                    x, y, gridsize=300, cmap="viridis", mincnt=1, norm=LogNorm()
                )
                fig.colorbar(hb, shrink=1, aspect=40, pad=0.02)

            ax.grid(
                True,
                which="both",
                linestyle="-",
                linewidth=0.7,
                alpha=0.4,
                color="grey",
            )

            # Fond transparent
            ax.set_facecolor((0, 0, 0, 0))
            fig.patch.set_alpha(0)
            ax.tick_params(axis="both", labelsize=14)

            st.pyplot(fig)
            st.write(f"Nombre de recettes affichées dans le graphe : {len(x)}")

        if "recipe_id" in self.dataframe.columns:
            with st.expander(
                f"Meilleures recettes selon le critère : {self.axis_y} (avec les filtres actuels)"
            ):
                display_df = self.dataframe[
                    self.dataframe["recipe_id"].isin(recipes_id)
                ]
                display_df = display_df.sort_values(by=self.axis_y, ascending=False)[
                    :10
                ]
                st.dataframe(display_df, hide_index=True)
        return True

    def display_graph(self, free=False, explanation=None):
        """
        Méthode pour afficher le graphique.

        :param free: condition pour choisir les axes et les filtres additionnels, defaults to False
        :type free: bool, optional
        :param explanation: explication du graphique, defaults to None
        :type explanation: str, optional
        :return: True si l'affichage a réussi
        :rtype: bool
        """
        self.default_values = self.default_values_save
        logger.info("Affichage du graphique pour l'instance avec key='%s'", self.key)
        chosen_filters = []
        range_filters = []
        if self.delete is False:
            with st.container(border=True):
                st.markdown(f"**{self.name}**")
                graph_container = st.empty()
                with graph_container.expander("**Filtres**", expanded=free):
                    if free is True:
                        axis_x, axis_y = self.__set_axis()
                    else:
                        axis_x = self.axis_x
                        axis_y = self.axis_y

                    self.range_axis_x = self.__set_range_axis(axis_x)
                    self.range_axis_y = self.__set_range_axis(axis_y)

                    if self.filters is not None and len(self.filters) > 0:
                        st.write("Filtres additionnels")
                        chosen_filters, range_filters = self.__filters(axis_x, axis_y)
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
                            if np.issubdtype(self.dataframe[axis_y].dtype, np.number):
                                self.log_axis_y = st.checkbox(
                                    "log axis_y",
                                    key=("log axis_y" + self.key + str(self.iteration)),
                                    value=self.log_axis_y,
                                )
                            else:
                                self.log_axis_y = False
                        if free is False:
                            col = st.columns(3)
                            with col[0]:
                                if st.form_submit_button(label="Tracer le graphe"):
                                    self.axis_x = axis_x
                                    self.axis_y = axis_y
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.axis_y,
                                            self.range_axis_x,
                                            self.range_axis_y,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )

                            if self.default_values_save is not None:
                                with col[1]:
                                    if st.form_submit_button(
                                        label="Réinitialiser le graphe"
                                    ):
                                        self.default_values = self.default_values_save
                                        self.axis_x = axis_x
                                        self.axis_y = axis_y
                                        range_filters_save = [
                                            self.default_values_save[filter]
                                            for filter in self.default_values_save[
                                                "chosen_filters"
                                            ]
                                        ]
                                        self.x, self.y, self.recipes_id = (
                                            self.get_data_points(
                                                self.dataframe,
                                                self.axis_x,
                                                self.axis_y,
                                                self.default_values_save[self.axis_x],
                                                self.default_values_save[self.axis_y],
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
                            col = st.columns(3)
                            with col[0]:
                                if st.form_submit_button(label="Tracer un graphe plot"):
                                    self.axis_x = axis_x
                                    self.axis_y = axis_y
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.axis_y,
                                            self.range_axis_x,
                                            self.range_axis_y,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )
                                    self.plot_type = "plot"

                            with col[1]:
                                if st.form_submit_button(
                                    label="Tracer un nuage de points"
                                ):
                                    self.axis_x = axis_x
                                    self.axis_y = axis_y
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.axis_y,
                                            self.range_axis_x,
                                            self.range_axis_y,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )
                                    self.plot_type = "scatter"

                            with col[2]:
                                if st.form_submit_button(
                                    label="Tracer une carte de densité"
                                ):
                                    self.axis_x = axis_x
                                    self.axis_y = axis_y
                                    self.x, self.y, self.recipes_id = (
                                        self.get_data_points(
                                            self.dataframe,
                                            self.axis_x,
                                            self.axis_y,
                                            self.range_axis_x,
                                            self.range_axis_y,
                                            chosen_filters,
                                            range_filters,
                                        )
                                    )
                                    self.plot_type = "density map"

                            col2 = st.columns(3)

                            with col2[0]:
                                if st.form_submit_button(label="Paramètres du graphe"):
                                    self.save_graph()

                            with col2[1]:
                                if st.form_submit_button(label=f"Supprimer le graphe"):
                                    self.delete = True
                                    logger.info(
                                        "Graphique supprime pour l'instance avec key='%s'",
                                        self.key,
                                    )
                                    st.rerun()

                if self.first_draw is True:
                    self.axis_x = axis_x
                    self.axis_y = axis_y
                    self.x, self.y, self.recipes_id = self.get_data_points(
                        self.dataframe,
                        self.axis_x,
                        self.axis_y,
                        self.range_axis_x,
                        self.range_axis_y,
                        chosen_filters,
                        range_filters,
                    )
                    self.first_draw = False

                self.__draw_plot(self.x, self.y, self.recipes_id)

                if explanation is not None:
                    st.write(explanation)

        return True
