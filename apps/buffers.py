import pandas as pd
import numpy as np
import geemap
import folium
import streamlit as st
import json
from streamlit_folium import folium_static
from data_cleaning import (
    cp_features
)
from mapping import (
    cp_allfeaturesmap,
    cp_featuresmap,
    all_colors,
    buffermap,
    squirrels_buffered_map
)
from buffer_analysis import buffer_features


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
    st.text("Buffer size: {1} * area ^ {0}".format(power, factor_slider))

    col1, col2 = st.columns(2)
    with col1:
        folium_static(buffermap, width=620, height=680)

    with col2:
        folium_static(squirrels_buffered_map, width=620, height=680)

    st.markdown("Display count of squirrels in each buffer as a bar graph")
    st.markdown("Small multiple graphs to show why we chose 0.4 and 1.2?")



