import streamlit as st
import streamlit.components.v1 as components
import geopandas as gpd
import folium
from streamlit_folium import folium_static


def app():
    st.title("Features in Central Park, NYC")

    st.subheader("All Features")

    st.markdown(
        """
        The shown features were retrieved from Open Street Map's data mining tool
        [overpass turbo](http://overpass-turbo.eu/). For every feature/layer pulled from OSM,
        the specific query was:
        - building: 
        - grass: `landuse=grass`
        - etc.
        """
    )

    with open('maps/cp_allfeaturesmap.html', 'r') as cp_all:
        cp_allfeatures_map = cp_all.read()

    components.html(cp_allfeatures_map, height=600)

    st.subheader("Relevant Features")

    st.markdown(
        """
        These are the relevant features we decided to choose to define a squirrel's
        geospatial relationship with Central Park: buildings, gardens, grass (like fields),
        pedestrian (walkways), water, streams, and woods.
        
        WHY: to simplify the amount of comparisons and in determining which feature a squirrel 
        was most associated with (overlap of too many features is complicated)
        """
    )
    with open('maps/cp_featuresmap.html', 'r') as cp_bare:
        cp_features_map = cp_bare.read()

    components.html(cp_features_map, height=600)

