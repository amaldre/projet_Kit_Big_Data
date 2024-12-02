import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Point
import pandas as pd
import numpy as np

# Titre de l'application
st.title("Carte des États-Unis avec GeoJSON et Points Aléatoires")

# Charger un fichier GeoJSON
geojson_path = "../data/us_states.geojson"  # Remplace par le chemin réel
gdf = gpd.read_file(geojson_path)

df_recette = pd.read_csv("../data/cloud_df.csv")

# Convertir la colonne "submitted" en datetime si nécessaire
df_recette["submitted"] = pd.to_datetime(df_recette["submitted"], errors="coerce")

# Extraire l'année
df_recette["année"] = df_recette["submitted"].dt.year

# Regrouper par année et compter le nombre de recettes
recettes_par_années = (
    df_recette.groupby("année").size().reset_index(name="nombre_recettes")
)

# Définir les limites du slider
année_min = 1999
année_max = 2019

# Initialiser la valeur du slider dans `session_state`
if "année" not in st.session_state:
    st.session_state.année = année_min

# Incrémenter automatiquement la valeur du slider avec `st_autorefresh`
refresh_rate = 1000  # En millisecondes
st_autorefresh = st.experimental_rerun()

# Mettre à jour l'année et la réinitialiser si elle dépasse le maximum
st.session_state.année += 1
if st.session_state.année > année_max:
    st.session_state.année = année_min

# Slider contrôlé par `session_state`
année_choisie = st.slider(
    "Choisissez une année",
    min_value=année_min,
    max_value=année_max,
    step=1,
    value=st.session_state.année,
)

# Nombre de recettes pour l'année choisie
nombre_recettes = recettes_par_années.loc[
    recettes_par_années["année"] == année_choisie, "nombre_recettes"
]
nombre_recettes = nombre_recettes.values[0] if not nombre_recettes.empty else 0

# Afficher le nombre de recettes
st.write(f"Année choisie : {année_choisie} avec {nombre_recettes} recettes.")

# Vérification des données
if gdf.empty:
    st.error("Le fichier GeoJSON est vide ou non valide.")
else:
    st.success("GeoJSON chargé avec succès.")

gdf["geometry"] = gdf["geometry"].simplify(0.2, preserve_topology=True)

# Combiner les géométries en une seule pour générer des points à l’intérieur
us_geometry = gdf.unary_union


# Générer des points aléatoires à l’intérieur des limites
def generate_points_in_geometry(geometry, n_points):
    points = []
    minx, miny, maxx, maxy = geometry.bounds
    while len(points) < n_points:
        random_point = Point(
            np.random.uniform(minx, maxx), np.random.uniform(miny, maxy)
        )
        if geometry.contains(random_point):
            points.append((random_point.x, random_point.y))
    return points


# Interface pour définir le nombre de points à générer
n_points = nombre_recettes // 10

# Générer les points
random_points = generate_points_in_geometry(us_geometry, n_points)

# Convertir en DataFrame pour Pydeck
df_points = pd.DataFrame(random_points, columns=["longitude", "latitude"])

# Couche GeoJSON pour les limites des États-Unis
geo_layer = pdk.Layer(
    "GeoJsonLayer",
    data=gdf.to_json(),
    pickable=True,
    stroked=True,
    filled=False,
    line_width_min_pixels=1,
)

# Couche pour les points
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_points,
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
deck = pdk.Deck(layers=[geo_layer, scatter_layer], initial_view_state=view_state)

# Afficher la carte
st.pydeck_chart(deck)

# Afficher les points sous forme de table
if st.checkbox("Afficher les données des points"):
    st.dataframe(df_points)
