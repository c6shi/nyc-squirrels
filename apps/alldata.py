import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datacleaning import (
    cp_allfeaturesmap,
    cp_featuresmap,
    cp_features,
    allcolors
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
        folium_static(cp_allfeaturesmap, height=700)
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

        # multi selection box
        relev_features = ['building', 'garden', 'grass', 'pedestrian', 'water', 'woods']
        features = st.multiselect("Choose relevant features in Central Park:", relev_features)
        if st.checkbox("Show all relevant features"):
            folium_static(cp_featuresmap, height=700)
        else:
            cp_selectfeatures_map = folium.Map(location=[40.7823, -73.96600],
                                               zoom_start=14,
                                               min_zoom=14,
                                               tiles='cartodbpositron',
                                               control_scale=True)
            for feature in features:
                folium.GeoJson(cp_features[cp_features['feature_type'] == feature],
                               name=feature,
                               style_function=lambda x: {'color': allcolors.get(feature),
                                                         'fillOpacity': 0.6}
                               ).add_to(cp_selectfeatures_map)

            folium.LayerControl().add_to(cp_selectfeatures_map)
            folium_static(cp_selectfeatures_map, height=700)
