import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static


def app():
    st.title("Data Analysis on Squirrels in Central Park, NYC")

    st.markdown(
        """
        In October 2018, a group of volunteers went out to Central Park to attempt 
        to record squirrel sightings. etc etc
        """
    )

    st.subheader("The Data Set")
    st.markdown(
        """
        Below is a map of all squirrels recorded in the 2018 Central Park Squirrel Census, 
        which can be downloaded from [NYC OpenData](https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw).
        """
    )
    nyc_gdf = gpd.read_file('dataframes/nycsquirrels_clean_1.csv')
    nyc_gdf = gpd.GeoDataFrame(nyc_gdf, geometry=gpd.points_from_xy(nyc_gdf.long, nyc_gdf.lat))
    nyc_gdf1 = nyc_gdf.set_crs('epsg:4326')

    raw_data_map = folium.Map(location=[40.7823, -73.96600],
                              zoom_start=14,
                              min_zoom=14,
                              tiles='cartodbpositron',
                              control_scale=True)

    all_squirrels = folium.FeatureGroup(name="squirrels")
    for i in range(len(nyc_gdf1)):
        folium.Circle(location=(nyc_gdf1.iloc[i]['lat'], nyc_gdf1.iloc[i]['long']),
                      radius=2).add_to(all_squirrels)
    all_squirrels.add_to(raw_data_map)

    folium_static(raw_data_map, width=620, height=680)

    st.subheader("Question: How do the different geographic features of Central Park affect squirrel's behaviors?")

    st.markdown(
        """
        1. getting outside data
        2. performing geospatial analysis/buffer analysis
        3. conducting permutation tests (our null hypothesis is...)
        """
    )
