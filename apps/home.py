import streamlit as st
from streamlit_folium import folium_static
from mapping import raw_data_map


def app():
    st.title("Data Analysis on Squirrels in Central Park, NYC")

    st.markdown(
        """
        In October 2018, a group of volunteers went out to Central Park to attempt 
        to record squirrel sightings. 
        """
    )

    st.subheader("The Data Set")
    st.markdown(
        """
        Below is a map of all squirrels recorded in the 2018 Central Park Squirrel Census, 
        which can be downloaded from [NYC OpenData](https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw).
        [The Squirrel Census](https://www.thesquirrelcensus.com/about) 
        is an organization that conducts squirrel counts and presents their findings in fun ways. 
        According to The Squirrel Census, the
        With the help of volunteers and 
        """
    )

    folium_static(raw_data_map, width=620, height=680)

    st.subheader("Question: How do the different geographic features of Central Park affect squirrel's behaviors?")

    st.markdown(
        """
        1. getting outside data
        2. performing geospatial analysis/buffer analysis
        3. conducting permutation tests (our null hypothesis is...)
        """
    )
