import pandas as pd
import numpy as np
import requests
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
    all_colors
)


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
        we expanded a squirrel's location in relation to feature to be ***near***
        a feature.
        """
    )

    # folium_static(test_map, height=700)


