"""
Ce module définit la classe de base pour les études de données.
"""

import math
import logging

import pandas as pd
import streamlit as st


logger = logging.getLogger(__name__)


class base_study:
    def __set_date(self, axis):
        """
        Create a date input range for datetime columns.

        :param axis: The column name to create the date input.
        :type axis: str
        :return: The start and end date selected.
        :rtype: Tuple[pd.Timestamp, pd.Timestamp]
        """
        min_date = self.dataframe[axis].min()
        max_date = self.dataframe[axis].max()
        if self.default_values is not None and axis in self.default_values:
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

    def __create_slider_from_df(self, df, axis):
        """
        Create a slider for numeric columns to select a range.

        :param df: The dataframe to get the min and max values.
        :type df: pd.DataFrame
        :param axis: The column name to create the slider.
        :type axis: str
        :return: The selected range.
        :rtype: Tuple[int, int]
        """
        data_min = math.floor(df[axis].min())
        data_max = math.ceil(df[axis].max())
        if self.default_values is not None and axis in self.default_values:
            default_value = self.default_values[axis]
        else:
            default_value = [data_min, data_max]

        logger.debug(
            "Creating a slider for '%s' with min=%d, max=%d", axis, data_min, data_max
        )
        return st.slider(
            label=f"Range for {axis}",
            min_value=data_min,
            max_value=data_max,
            value=default_value,
            step=1,
            key=(axis + self.key + str(self.iteration)),
        )
