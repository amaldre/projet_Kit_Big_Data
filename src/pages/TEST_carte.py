import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Point
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import altair as alt


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")


st.title("Carte Data Food.com au cours des années")


@st.cache_data
def load_geojson(path):
    gdf = gpd.read_file(path)
    gdf["geometry"] = gdf["geometry"].simplify(0.2, preserve_topology=True)
    return gdf


@st.cache_data
def load_recipes_data(path):
    df = pd.read_csv(path)
    df["submitted"] = pd.to_datetime(df["submitted"], errors="coerce")
    df["année"] = df["submitted"].dt.year
    return df


@st.cache_data
def generate_random_points(recettes_par_années, _gdf):
    us_geometry = _gdf.union_all()
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

geojson_path = "../data/us_states.geojson"
gdf = load_geojson(geojson_path)
us_geometry = gdf.union_all()

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

text_data = pd.DataFrame(
    {"latitude": [49], "longitude": [-70], "text": [str(st.session_state.année)]}
)

text_layer = pdk.Layer(
    "TextLayer",
    data=text_data,
    get_position=["longitude", "latitude"],
    get_text="text",
    get_size=24,
    get_color=[255, 140, 0],
    get_angle=0,
    get_text_anchor='"start"',
    get_alignment_baseline='"top"',
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
            top: 20px;  /* Adjust as needed */
            right: 50px; /* Adjust as needed */
            font-size: 48px;
            color: orange;
            z-index: 9999;
            pointer-events: none;  /* Allow map interactions */
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
