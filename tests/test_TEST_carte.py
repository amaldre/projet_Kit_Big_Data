from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import pandas.testing as pdt
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point, Polygon

from src.pages.Simulation_Carte import (
    main,
    load_geojson,
    load_recipes_data,
    generate_random_points,
    create_scrolling_banner,
)


def test_create_scrolling_banner():
    texte = "Test Banner"
    expected_html = """
        <style>
        .scrolling-banner {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: #f0f2f6; /* Couleur de fond du bandeau */
            overflow: hidden;
            height: 50px; /* Hauteur du bandeau */
            z-index: 9999; /* Assure que le bandeau reste au-dessus des autres elements */
        }

        .scrolling-banner h1 {
            position: absolute;
            width: 100%;
            height: 50px;
            line-height: 50px;
            margin: 0;
            font-size: 24px;
            color: #4CAF50; /* Couleur du texte */
            text-align: center;
            transform: translateX(100%);
            animation: scroll-left 10s linear infinite;
        }

        /* Animation pour le defilement du texte */
        @keyframes scroll-left {
            from {
                transform: translateX(100%);
            }
            to {
                transform: translateX(-100%);
            }
        }
        </style>

        <div class="scrolling-banner">
            <h1>Test Banner</h1>
        </div>
        """
    result = create_scrolling_banner(texte)
    assert result.strip() == expected_html.strip()


@pytest.fixture
def mock_geojson_read():
    data = {"geometry": [None]}
    mock_gdf = gpd.GeoDataFrame(data)
    return mock_gdf


def test_load_geojson(mock_geojson_read):
    with patch("geopandas.read_file", return_value=mock_geojson_read) as mock_read_file:
        path = "data/us_states.geojson"
        result = load_geojson(path)

        assert result.equals(mock_geojson_read)
        mock_read_file.assert_called_once_with(path)


def test_load_recipes_data():
    mock_csv_read = pd.DataFrame(
        {
            "submitted": ["2021-01-01", "2021-01-02"],
        }
    )
    with patch("pandas.read_csv", return_value=mock_csv_read) as mock_read_csv:
        path = "data/cloud_df.csv"
        result = load_recipes_data(path)

        print("Result:", result)
        print("Mock CSV Read:", mock_csv_read)

        pd.testing.assert_frame_equal(result, mock_csv_read)
        mock_read_csv.assert_called_once_with(path)


@pytest.fixture
def mock_geojson():
    from shapely.geometry import box

    return gpd.GeoDataFrame(
        {"geometry": [box(-100, 30, -90, 40)]},
    )


@pytest.fixture
def mock_recipes_data():
    return pd.DataFrame({"année": [2020, 2021], "nombre_recettes": [100, 200]})


@pytest.fixture
def mock_gdf():
    polygon = Polygon([(-100, 30), (-100, 40), (-90, 40), (-90, 30)])
    gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="EPSG:4326")
    return gdf


def test_generate_random_points_normal(mock_recipes_data, mock_gdf):
    result = generate_random_points(mock_recipes_data, mock_gdf)

    assert isinstance(result, pd.DataFrame)
    assert "longitude" in result.columns
    assert "latitude" in result.columns
    assert "année" in result.columns
    assert len(result) == 30


def test_generate_random_points_exception_handling(mock_recipes_data):

    try:
        generate_random_points(mock_recipes_data, None)
    except Exception as e:
        pytest.fail(f"main() a levé une exception: {e}")


@patch("streamlit.title")
@patch("streamlit.write")
@patch("streamlit.success")
@patch("streamlit.error")
@patch("streamlit.slider")
@patch("streamlit.checkbox")
@patch("src.pages.Simulation_Carte.load_geojson")
@patch("src.pages.Simulation_Carte.load_recipes_data")
@patch("src.pages.Simulation_Carte.generate_random_points")
def test_main(
    mock_generate_random_points,
    mock_load_recipes_data,
    mock_load_geojson,
    mock_checkbox,
    mock_slider,
    mock_st_error,
    mock_st_success,
    mock_st_write,
    mock_st_title,
    mock_geojson,
    mock_recipes_data,
):
    mock_gdf = mock_geojson
    mock_recipes_df = mock_recipes_data
    mock_load_geojson.return_value = mock_gdf
    mock_load_recipes_data.return_value = mock_recipes_df
    mock_generate_random_points.return_value = pd.DataFrame(
        {"longitude": [-98.0, -97.0], "latitude": [35.0, 36.0], "année": [2020, 2021]}
    )
    mock_slider.return_value = 2020
    mock_checkbox.return_value = True

    main()

    mock_st_title.assert_any_call("Carte Data Food.com au cours des années")
    mock_st_success.assert_any_call("GeoJSON chargé avec succès.")
    assert mock_st_write.call_count == 2

    expected_df = pd.DataFrame(
        {
            "année": [2020, 2021],
            "nombre_recettes": [1, 1],
            "is_current_year": [False, True],
        }
    )
    print(expected_df)
    print(mock_generate_random_points.call_args[0][0])
    pdt.assert_frame_equal(mock_generate_random_points.call_args[0][0], expected_df)
    mock_st_error.assert_not_called()
    assert mock_generate_random_points.return_value.shape == (2, 3)
