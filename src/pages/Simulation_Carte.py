"""
Page de visualisation des données sous forme d'une carte interactive.
"""

import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Point
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import altair as alt
import logging
import os
from utils.load_functions import load_css

logger = logging.getLogger(os.path.basename(__file__))
st.set_page_config(
    page_title="MangeTaData", page_icon="images/favicon_mangetadata.png", layout="wide"
)

load_css("src/style.css")


@st.cache_data
def load_geojson(path):
    """
    Load a GeoJSON file

    :param path: path of the GeoJSON file
    :type path: str
    :return: GeoDataFrame containing the GeoJSON data
    :rtype: gpd.GeoDataFrame
    """
    try:
        gdf = gpd.read_file(path)
        gdf["geometry"] = gdf["geometry"].simplify(0.2, preserve_topology=True)
        logger.info(f"GeoJSON chargé avec succès depuis {path}.")
        return gdf
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier GeoJSON : {path}. {e}")
        st.error("Erreur lors du chargement des données géographiques.")
        return gpd.GeoDataFrame()


@st.cache_data
def load_recipes_data(path):
    """
    Charge les données de recettes soumises et retourne un DataFrame

    :param path: chemin vers le fichier CSV
    :type path: str
    :return: DataFrame contenant les données de recettes
    :rtype: pd.DataFrame
    """
    try:
        df = pd.read_csv(path)
        df["Date de publication de la recette"] = pd.to_datetime(df["Date de publication de la recette"], errors="coerce")
        df["année"] = df["Date de publication de la recette"].dt.year
        logger.info(f"Données de recettes chargées avec succès depuis {path}.")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données de recettes : {path}. {e}")
        st.error("Erreur lors du chargement des données de recettes.")
        return pd.DataFrame()


@st.cache_data
def generate_random_points(recettes_par_années, _gdf):
    """
    Génère des points aléatoires à l'intérieur de la géométrie des États-Unis
    en fonction du nombre de recettes soumises chaque année.

    :param recettes_par_années: DataFrame contenant le nombre de recettes par année
    :type recettes_par_années: pd.DataFrame
    :param _gdf: GeoDataFrame contenant la géométrie des États-Unis
    :type _gdf: gpd.GeoDataFrame
    :return: DataFrame contenant les points aléatoires
    :rtype: pd.DataFrame
    """
    try:
        us_geometry = _gdf.union_all()
        data_points = []

        for _, row in recettes_par_années.iterrows():
            année = row["année"]
            nombre_recettes = row["nombre_recettes"]
            n_points = max(nombre_recettes // 10, 1)

            points = []
            minx, miny, maxx, maxy = us_geometry.bounds
            attempts = 0
            max_attempts = n_points * 10
            while len(points) < n_points and attempts < max_attempts:
                random_point = Point(
                    np.random.uniform(minx, maxx), np.random.uniform(miny, maxy)
                )
                if us_geometry.contains(random_point):
                    points.append(
                        {
                            "longitude": random_point.x,
                            "latitude": random_point.y,
                            "année": année,
                        }
                    )
                attempts += 1

            data_points.extend(points)

        df_points = pd.DataFrame(data_points)
        logger.info("Points aléatoires générés avec succès.")
        return df_points
    except Exception as e:
        logger.error(f"Erreur lors de la génération de points aléatoires : {e}")
        st.error("Erreur lors de la génération des points aléatoires.")
        return pd.DataFrame()


def main():

    st.title("Carte Data Food.com au cours des années")

    st.write(
        """
        Cette carte illustre le défi majeur auquel le site est confronté : 
        la diminution de sa base d'utilisateurs. 
        Les points sur la carte ne représentent pas les localisations réelles des utilisateurs, 
        mais servent uniquement de visualisation symbolique. Chaque point correspond à 10 recettes soumises, 
        mettant en lumière les tendances d'engagement des utilisateurs au fil du temps. 
        Cette représentation permet d'identifier visuellement les périodes de croissance et 
        de déclin pour mieux orienter les efforts de reconquête et d'amélioration.
        """
    )

    geojson_path = "data/us_states.geojson"
    gdf = load_geojson(geojson_path)

    df_recette = load_recipes_data("data/clean_cloud_df.csv")

    if gdf.empty:
        st.error("Le fichier GeoJSON est vide ou non valide.")
    else:
        st.success("GeoJSON chargé avec succès.")

    recettes_par_années = (
        df_recette.groupby("année").size().reset_index(name="nombre_recettes")
    )

    df_points = generate_random_points(recettes_par_années, gdf)

    if df_points.empty:
        st.error("Aucun point généré pour l'affichage.")

    année_min = int(df_points["année"].min()) if not df_points.empty else 0
    année_max = int(df_points["année"].max()) if not df_points.empty else 0

    if "animation_running" not in st.session_state:
        st.session_state.animation_running = False
    if "année" not in st.session_state:
        st.session_state.année = année_min

    st.session_state.animation_running = st.checkbox(
        "Démarrer l'animation",
        value=st.session_state.animation_running,
    )

    if st.session_state.animation_running:
        st_autorefresh(interval=1000, key="animation_refresh")
        st.session_state.année += 1
        if st.session_state.année > année_max:
            st.session_state.année = année_min
    else:
        année_choisie = st.slider(
            "Choisissez une année",
            min_value=année_min,
            max_value=année_max,
            step=1,
            value=st.session_state.année,
        )
        st.session_state.année = année_choisie

    df_points_filtered = df_points[df_points["année"] == st.session_state.année]

    nombre_recettes = recettes_par_années.loc[
        recettes_par_années["année"] == st.session_state.année, "nombre_recettes"
    ]
    nombre_recettes = nombre_recettes.values[0] if not nombre_recettes.empty else 0

    st.write(
        f"Année choisie : {st.session_state.année} avec {nombre_recettes} recettes."
    )

    geo_layer = pdk.Layer(
        "GeoJsonLayer",
        data=gdf,
        pickable=True,
        stroked=True,
        filled=False,
        line_width_min_pixels=1,
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_points_filtered,
        get_position=["longitude", "latitude"],
        get_radius=20000,
        get_color="[255, 140, 0, 200]",
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=37.0902,
        longitude=-95.7129,
        zoom=3,
        pitch=0,
    )

    with st.container():
        st.markdown(
            f"""
            <style>
            .year-overlay {{
                position: absolute;
                top: 20px;  
                right: 50px;
                font-size: 48px;
                color: orange;
                z-index: 9999;
                pointer-events: none;
            }}
            </style>
            <div class="year-overlay">{st.session_state.année}</div>
            """,
            unsafe_allow_html=True,
        )

        deck = pdk.Deck(
            layers=[geo_layer, scatter_layer],
            initial_view_state=view_state,
        )
        st.pydeck_chart(deck)

    recettes_par_années["is_current_year"] = (
        recettes_par_années["année"] == st.session_state.année
    )

    chart = (
        alt.Chart(recettes_par_années)
        .mark_bar()
        .encode(
            x=alt.X("année:O", title="Année"),
            y=alt.Y("nombre_recettes:Q", title="Nombre de recettes"),
            color=alt.condition(
                alt.datum.is_current_year, alt.value("orange"), alt.value("steelblue")
            ),
        )
        .properties(width=600, height=400, title="Nombre de recettes par année")
    )

    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()