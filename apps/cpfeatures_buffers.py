import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import folium
import streamlit as st
import json
from streamlit_folium import folium_static
from shapely import wkt


# Title
st.title("Central Park Features")

# Header
st.header("This is a header")

# Text
st.text("data from the Squirrel Census")

# Markdown
st.markdown("### This is a markdown")

# checkbox
if st.checkbox("Show/Hide"):
    st.text("Showing the widget")

# radio button
status = st.radio("Select Gender: ", ("Male", "Female"))
if (status == "Male"):
    st.success("Male")
else:
    st.success("Female")

# selection box
relev_features = ['building', 'garden', 'grass', 'pedestrian', 'water', 'woods']
feature = st.selectbox("relevant features in Central Park: ", relev_features)

# multi selection box
features = st.multiselect("relevant features in Central Park: ", relev_features)
st.write("You selected", len(features), "features")

# button
if (st.button("About")):
    st.text("So what, squirrels?")

# slider
level = st.slider("Select the buffer size", 1, 5)
st.text("Buffer size: {}".format(level))

"# central park features"

cp_allpd = pd.read_csv('dataframes/cp_allfeatures.csv')
cp_allpd['geometry'] = cp_allpd['geometry'].apply(wkt.loads)

cp_pd = pd.read_csv('dataframes/cp_features.csv')
cp_pd['geometry'] = cp_pd['geometry'].apply(wkt.loads)

cp_allfeatures = gpd.GeoDataFrame(cp_allpd, crs='epsg:4326')
cp_features = gpd.GeoDataFrame(cp_pd, crs='epsg:4326')


cp_allfeaturesmap = folium.Map(location=[40.7823, -73.96600],
                               zoom_start=14,
                               min_zoom=14,
                               tiles='cartodbpositron',
                               control_scale=True)


def to_geojson_map(df, feature, folium_map, color_var, fillOp):
    gen_stylefunc = lambda x: {'color': color_var, 'fillOpacity': fillOp}
    to_geojson = folium.GeoJson(df[df['feature_type'] == feature], name=feature, style_function=gen_stylefunc)
    to_geojson.add_to(folium_map)
    return


allfeatures = list(cp_allfeatures['feature_type'].unique())
allcolors = {'building': '#ad6f03',
             'garden': '#ff8cec',
             'grass': '#86b35d',
             'pedestrian': '#000000',
             'water': '#1795e8',
             'stream': '#1795e8',
             'woods': '#098f57',
             'paved': '#000000',
             'pitch: baseball': '#e0cdb4',
             'playground': '#f5931b',
             'sports center': '#960000',
             'bare_rock': '#525252',
             'toilet': '#103b91'}

for i in range(len(allfeatures)):
    to_geojson_map(cp_allfeatures, allfeatures[i], cp_allfeaturesmap, allcolors[allfeatures[i]], 0.6)

folium.LayerControl().add_to(cp_allfeaturesmap)

folium_static(cp_allfeaturesmap)

