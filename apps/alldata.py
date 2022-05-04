import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static


def app():
    st.title("Features in Central Park, NYC")

    with open('maps/cp_allfeaturesmap.html', 'r') as cp_all:
        cp_allfeatures_map = cp_all.read()

    with open('maps/cp_featuresmap.html', 'r') as cp_bare:
        cp_features_map = cp_bare.read()

    cp_allfeatures = pd.read_csv('dataframes/cp_allfeatures.csv')
    cp_features = pd.read_csv('dataframes/cp_features.csv')

    featuremap_selection = st.radio("Select a map", ("All Features", "Relevant Features"))
    if featuremap_selection == "All Features":
        st.markdown(
            """
            #### All Features
            
            The shown features were retrieved from Open Street Map's data mining tool
            [overpass turbo](http://overpass-turbo.eu/). For every feature/layer pulled from OSM,
            the specific query was:
            - building: `building=yes` and `building=museum` (for the MET)
            - garden: `leisure=garden`
            - grass: `landuse=grass`
            - pedestrian: `highway=pedestrian` (perhaps more humans are located here)
            - water: `natural=water`
            - stream: `waterway=stream`
            - woods: `natural=wood`
            - ... etc.
            """
        )
        components.html(cp_allfeatures_map, height=600)
    else:
        st.markdown(
            """
            #### Relevant Features
            
            These are the relevant features we decided to choose to define a squirrel's
            geospatial relationship with Central Park: buildings, gardens, grass (like fields),
            pedestrian (walkways), water, streams, and woods.

            WHY: to simplify the amount of comparisons and in determining which feature a squirrel 
            was most associated with (overlap of too many features is complicated)
            """
        )

        # multi selection box
        relev_features = ['building', 'garden', 'grass', 'pedestrian', 'water', 'woods']
        features = st.multiselect("Choose relevant features in Central Park:", relev_features)

        components.html(cp_features_map, height=600)

