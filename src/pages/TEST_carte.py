import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Point
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# Titre de l'application
st.title("Carte des États-Unis avec GeoJSON et Points Aléatoires")


# Charger les données GeoJSON
@st.cache_data
def load_geojson(path):
    gdf = gpd.read_file(path)
    gdf["geometry"] = gdf["geometry"].simplify(0.2, preserve_topology=True)
    return gdf


# Charger les données de recettes
@st.cache_data
def load_recipes_data(path):
    df = pd.read_csv(path)
    df["submitted"] = pd.to_datetime(df["submitted"], errors="coerce")
    df["année"] = df["submitted"].dt.year
    return df


# Générer des points pour toutes les années
@st.cache_data
def generate_random_points(recettes_par_années, _gdf):
    us_geometry = _gdf.unary_union
    data_points = []

    for idx, row in recettes_par_années.iterrows():
        année = row["année"]
        nombre_recettes = row["nombre_recettes"]
        n_points = max(nombre_recettes // 10, 1)  # Au moins un point

        # Générer des points aléatoires à l'intérieur de la géométrie des États-Unis
        points = []
        minx, miny, maxx, maxy = us_geometry.bounds
        attempts = 0
        max_attempts = n_points * 10  # Éviter les boucles infinies
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
    return df_points


# Charger les données
geojson_path = "../data/us_states.geojson"  # Remplace par le chemin réel
gdf = load_geojson(geojson_path)
us_geometry = gdf.unary_union

df_recette = load_recipes_data("../data/cloud_df.csv")

# Regrouper par année et compter le nombre de recettes
recettes_par_années = (
    df_recette.groupby("année").size().reset_index(name="nombre_recettes")
)

# Générer les points pour toutes les années
df_points = generate_random_points(recettes_par_années, gdf)

# Vérification des données
if gdf.empty:
    st.error("Le fichier GeoJSON est vide ou non valide.")
else:
    st.success("GeoJSON chargé avec succès.")

# Définir les limites du slider
année_min = int(df_points["année"].min())
année_max = int(df_points["année"].max())

# Initialiser les variables d'état
if "animation_running" not in st.session_state:
    st.session_state.animation_running = False
if "année" not in st.session_state:
    st.session_state.année = année_min

# Checkbox pour démarrer/arrêter l'animation
st.session_state.animation_running = st.checkbox(
    "Démarrer l'animation",
    value=st.session_state.animation_running,
)

# Contrôler l'animation
if st.session_state.animation_running:
    # Rafraîchir automatiquement toutes les 1 seconde
    st_autorefresh(interval=1000, key="animation_refresh")
    # Incrémenter l'année
    st.session_state.année += 1
    if st.session_state.année > année_max:
        st.session_state.année = année_min
else:
    # Slider pour sélectionner l'année
    année_choisie = st.slider(
        "Choisissez une année",
        min_value=année_min,
        max_value=année_max,
        step=1,
        value=st.session_state.année,
    )
    st.session_state.année = année_choisie

# Filtrer les points pour l'année choisie
df_points_filtered = df_points[df_points["année"] == st.session_state.année]

# Nombre de recettes pour l'année choisie
nombre_recettes = recettes_par_années.loc[
    recettes_par_années["année"] == st.session_state.année, "nombre_recettes"
]
nombre_recettes = nombre_recettes.values[0] if not nombre_recettes.empty else 0

# Afficher le nombre de recettes
st.write(f"Année choisie : {st.session_state.année} avec {nombre_recettes} recettes.")

# Couche GeoJSON pour les limites des États-Unis
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

# Vue initiale
view_state = pdk.ViewState(
    latitude=37.0902,  # Centre approximatif des États-Unis
    longitude=-95.7129,
    zoom=3,
    pitch=0,
)

# Ajouter les couches à Pydeck
deck = pdk.Deck(
    layers=[geo_layer, scatter_layer],
    initial_view_state=view_state,
)

# Afficher la carte
st.pydeck_chart(deck)
