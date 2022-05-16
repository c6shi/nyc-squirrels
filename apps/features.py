import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from data_cleaning import (
    cp_features,
    relev_features
)
from mapping import (
    cp_allfeaturesmap,
    cp_featuresmap,
    all_colors
)


def app():
    st.title("Features in Central Park, NYC")

    # choosing between ALL FEATURES or RELEVANT FEATURES
    featuremap_selection = st.radio("Select a map", ("All Features", "Relevant Features"))
    if featuremap_selection == "All Features":
        st.markdown(
            """
            #### All Features
            
            The shown features were retrieved from Open Street Map's data mining tool
            [overpass turbo](http://overpass-turbo.eu/). For every feature/layer pulled from OSM,
            the specific query was:
            - building: `building=yes` and `building=museum` (for the Metropolitan)
            - garden: `leisure=garden`
            - grass: `landuse=grass`
            - pedestrian: `highway=pedestrian` (perhaps more humans are located here)
            - water: `natural=water`
            - stream: `waterway=stream`
            - woods: `natural=wood`
            - ... etc.
            """
        )
        folium_static(cp_allfeaturesmap, width=620, height=680)
    else:
        # choosing INDIVIDUAL RELEVANT FEATURES
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

        folium_static(cp_featuresmap, width=620, height=680)
