import streamlit as st
import math
import matplotlib.pyplot as plt
import logging
import pandas as pd

# Créez un logger spécifique pour ce module
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="app.log",  # Nom du fichier de log
    filemode="a",  # Mode append pour ajouter au fichier sans l'écraser
    level=logging.INFO,  # Niveau minimum des messages de log à enregistrer
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format des messages
    datefmt="%Y-%m-%d %H:%M:%S",  # Format de la date
)


class bivariateStudy:

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
        self.name = key if name == None else name
        self.default_values = default_values
        self.default_values_save = default_values
        self.chosen_filters = None
        self.range_filters = None

        # Log l'initialisation de l'objet
        logger.info("Instance de Study créée avec key='%s'", self.key)

    def __del__(self):
        logger.info("Instance de Study avec key='%s' supprimée", self.key)
        return

    # Méthode d'affichage des attributs
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
            f'axis_x={self.axis_x}, axis_y={self.axis_y}, filters={self.chosen_filters}, plot_type="{self.plot_type}", '
            + "default_values={"
            + f'{self.axis_x}": {self.range_axis_x},\
                "{self.axis_y}": {self.range_axis_y}, '
            + range_filters
            + f'", chosen_filters":{self.chosen_filters}'
            + "}"
        )
        print(output)
        st.write(output)

    def __set_axis(self):
        axis_y = st.selectbox(label=f"axis_y ({self.key})", options=self.axis_y_list)
        axis_x = st.selectbox(label=f"axis_x ({self.key})", options=self.axis_x_list)
        logger.debug("Axes définis: axis_x=%s, axis_y=%s", axis_x, axis_y)
        return axis_x, axis_y

    def __create_slider_from_df(self, df, column):

        min = math.floor(df[column].min())
        max = math.ceil(df[column].max())
        if self.default_values != None and column in self.default_values:
            default_value = self.default_values
        else:
            default_value = [min, max]
        logger.debug(
            "Création d'un slider pour '%s' avec min=%d, max=%d", column, min, max
        )
        return st.slider(
            label=f"Range for {column} ({self.key})",
            min_value=min,
            max_value=max,
            value=default_value,
            step=1,
        )

    def __set_date(self, axis):
        min_date = self.dataframe[axis].min()
        max_date = self.dataframe[axis].max()
        if self.default_values != None and axis in self.default_values:
            default_value = self.default_values
        else:
            default_value = [min_date, max_date]
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                f"Start date ({self.key})",
                value=default_value[0],
                min_value=min_date,
                max_value=max_date,
            )
        with col2:
            end_date = st.date_input(
                f"End date ({self.key})",
                value=default_value[1],
                min_value=start_date,
                max_value=max_date,
            )
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return start_date, end_date

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
        columns = [axis_x, axis_y] + chosen_filters
        if "id" in df.columns:
            columns += ["id"]
        df = df[columns].sort_values(by=axis_x)
        df = df[(df[axis_x] >= range_axis_x[0]) & (df[axis_x] <= range_axis_x[1])]
        df = df[(df[axis_y] >= range_axis_y[0]) & (df[axis_y] <= range_axis_y[1])]
        if len(chosen_filters) > 0:
            for i, filter in enumerate(chosen_filters):
                df = df[
                    (df[filter] >= range_filters[i][0])
                    & (df[filter] <= range_filters[i][1])
                ]
        if "recipe_id" in self.dataframe.columns:
            return df[axis_x].values, df[axis_y].values, df["recipe_id"].values
        else:
            return df[axis_x].values, df[axis_y].values, df["id"].values

    def __set_range_axis(self, axis):
        print("________\n", self.dataframe[axis].head())
        if self.dataframe[axis].dtype == "datetime64[ns]":
            range_axis = self.__set_date(axis)
        else:
            range_axis = self.__create_slider_from_df(self.dataframe, axis)
        logger.debug(f"Plages définies pour axis {axis}: range_axis_x= {range_axis}")
        return range_axis

    def __filters(self, axis_x, axis_y):
        if self.default_values != None:
            default_values = self.default_values["chosen_filters"]
        else:
            default_values = None
        filters = [
            filtre for filtre in self.filters if (filtre != axis_x and filtre != axis_y)
        ]
        chosen_filters = st.multiselect(
            label=f"filters ({self.key})", default=default_values, options=filters
        )
        range_filters = []
        for filter in chosen_filters:
            range_axis = self.__set_range_axis(filter)
            range_filters.append(range_axis)
        logger.debug("Filtres choisis : %s", chosen_filters)

        return chosen_filters, range_filters

    def __draw_plot(self, x, y, recipes_id):
        col = st.columns([1, 3, 1])
        with col[1]:
            # Create a figure
            fig = plt.figure(figsize=(10, 6))
            plt.title(self.name)
            plt.xlabel(self.axis_x)
            plt.ylabel(self.axis_y)
            if self.plot_type == "scatter":
                plt.scatter(x, y, s=1)
            elif self.plot_type == "plot":
                plt.plot(x, y)
            st.pyplot(fig)
            st.write(f"number of data points : {len(x)}")

        if "recipe_id" in self.dataframe.columns:
            st.write(f"number of data point : {len(self.x)}")
            with st.expander(f"Dataframe best {self.axis_y} ({self.key})"):
                display_df = self.dataframe[
                    self.dataframe["recipe_id"].isin(recipes_id)
                ]
                display_df = display_df.sort_values(by=self.axis_y, ascending=False)[
                    :10
                ]
                st.dataframe(display_df, hide_index=True)

    # Affichage pour les graphes d'intérêt à navigation limité
    def display_graph(self, free=False):
        logger.info("Affichage du graphique pour l'instance avec key='%s'", self.key)
        chosen_filters = []
        range_filters = []

        if self.delete == False:
            with st.container(border=True):
                st.markdown(f"**{self.name}**")
                if st.checkbox(f"hide filters ({self.key})") != True:
                    if free == True:
                        self.axis_x, self.axis_y = self.__set_axis()
                    self.range_axis_x = self.__set_range_axis(self.axis_x)
                    self.range_axis_y = self.__set_range_axis(self.axis_y)
                    if self.filters != None:
                        st.write("extra_filters")
                        chosen_filters, range_filters = self.__filters(
                            self.axis_x, self.axis_y
                        )
                        self.chosen_filters = chosen_filters
                        self.range_filters = range_filters

                    with st.form(self.key, border=False):
                        col = st.columns(3)
                        place_button = 0
                        with col[place_button]:
                            if st.form_submit_button(label=f"Draw graph ({self.key})"):
                                print("there")

                                self.x, self.y, self.recipes_id = self.get_data_points(
                                    self.dataframe,
                                    self.axis_x,
                                    self.axis_y,
                                    self.range_axis_x,
                                    self.range_axis_y,
                                    chosen_filters,
                                    range_filters,
                                )
                                self.default_values = None
                            place_button += 1

                        if self.default_values_save != None:
                            with col[place_button]:
                                if st.form_submit_button(
                                    label=f"Reset graph ({self.key})"
                                ):
                                    self.default_values = self.default_values_save
                            place_button += 1

                        if free == True:
                            with col[place_button]:
                                if st.form_submit_button(
                                    label=f"Save graph ({self.key})"
                                ):
                                    self.save_graph()
                            place_button += 1

                        if free == True:
                            with col[place_button]:
                                if st.form_submit_button(
                                    label=f"Delete graph ({self.key})"
                                ):
                                    self.delete = True
                                    logger.info(
                                        "Graphique supprimé pour l'instance avec key='%s'",
                                        self.key,
                                    )
                                    st.rerun()

                if self.first_draw == True:
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
