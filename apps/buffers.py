import pandas as pd
import numpy as np
import geemap
import folium
import streamlit as st
import plotly.express as px
import geopandas as gpd
from streamlit_folium import folium_static
from data_cleaning import (
    cp_features,
    relev_features,
    behaviors
)
from mapping import (
    cp_allfeaturesmap,
    cp_featuresmap,
    all_colors,
    featuregroup_to_map,
    geojson_to_map_obj
)
from buffer_analysis import calculate_buffer_radius, buffer_analysis, nyc_gdf1, geospatial_analysis


def app():
    st.title("Defining a Squirrel's Geospatial Relationship with Central Park")

    st.subheader("Buffers: Near vs In")

    st.markdown(
        """
        One way to quantify a squirrel's geographic relationship with Central Park
        is to determine whether a squirrel is inside a certain geographic feature.
        For example, a squirrel can be inside the woods, and we could label all the 
        squirrels inside the woods and categorize them like so. 
        
        However, some features like water bodies do not allow squirrels to be ***in***
        them. Rather, they could be near the water body and still be more associated 
        with the water feature than a squirrel far away from the water body. Hence,
        we expanded a squirrel's location in relation to a feature to be ***near***
        a feature.
        """
    )

    power = st.slider("Select the buffer power:", 0.1, 1.0, step=0.05)
    factor_slider = st.slider("Select the buffer factor:", 0.1, 4.0, step=0.1)

    # buffer interaction
    planar_features = cp_features.to_crs('epsg:2263')
    planar_features['area'] = planar_features.geometry.area

    planar_features['buffer_radius'] = planar_features['area'].apply(
        calculate_buffer_radius, power=power, factor=factor_slider, cap=150, base=50)

    buffer_features = buffer_analysis(nyc_gdf1, planar_features)

    buffered_nyc_df = nyc_gdf1[['long', 'lat', 'geometry'] + behaviors + geospatial_analysis].to_crs('epsg:4326')

    bfsqrls = buffered_nyc_df.query('nearbuilding == True '
                                    'or neargarden == True '
                                    'or neargrass == True '
                                    'or nearpedestrian == True '
                                    'or nearwater == True '
                                    'or nearwoods == True'
                                    ).reset_index().drop(columns='index')

    bfsqrls = bfsqrls.drop(columns=['kuks', 'quaas', 'moans', 'tail_flags', 'approaches', 'chasing'])

    buffermap = folium.Map(
        location=[40.7823, -73.96600],
        zoom_start=14,
        min_zoom=14,
        tiles='cartodbpositron',
        control_scale=True
    )

    for relev_feature in relev_features:
        buffer_fg = featuregroup_to_map(
            buffer_features,
            relev_feature,
            buffermap,
            all_colors[relev_feature],
            0.2
        )
        geojson_to_map_obj(
            cp_features,
            relev_feature,
            buffer_fg,
            all_colors[relev_feature],
            0.6
        )

    folium.LayerControl().add_to(buffermap)

    st.text("Buffer size: {1} * area ^ {0}".format(power, factor_slider))

    squirrels_buffered_map = folium.Map(
        location=[40.7823, -73.96600],
        zoom_start=14,
        min_zoom=14,
        tiles='cartodbpositron',
        control_scale=True
    )

    squirrels_in_buffer = folium.FeatureGroup(name='squirrels remaining')
    squirrels_notin_buffer = folium.FeatureGroup(name='all squirrels')

    for i in range(len(bfsqrls)):
        folium.Circle(
            location=(bfsqrls.iloc[i]['lat'], bfsqrls.iloc[i]['long']),
            color='#FF4B4B',
            radius=2).add_to(squirrels_in_buffer)

    for i in range(len(nyc_gdf1)):
        folium.Circle(
            location=(nyc_gdf1.iloc[i]['lat'], nyc_gdf1.iloc[i]['long']),
            color='gray',
            radius=2).add_to(squirrels_notin_buffer)

    squirrels_notin_buffer.add_to(squirrels_buffered_map)
    squirrels_in_buffer.add_to(squirrels_buffered_map)

    col1, col2 = st.columns(2)
    with col1:
        folium_static(buffermap, width=620, height=680)

    with col2:
        folium_static(squirrels_buffered_map, width=620, height=680)

    below_map = px.bar(bfsqrls[geospatial_analysis].sum(), text_auto=True)
    st.plotly_chart(below_map)

    st.markdown("Small multiple graphs to show why we chose 0.4 and 1.2?")
