import geopandas as gpd
import folium
import shapely
from shapely.ops import transform
from shapely.geometry import mapping
from folium import Popup, Tooltip
from data_cleaning import (
    nyc_gdf,
    nyc_gdf1,
    cp_allfeatures,
    cp_features,
    relev_features
)
from buffer_analysis import buffer_features, bfsqrls


# 1) DEFINE FUNCTIONS FOR GENERALIZED MAPPING


# a) GeoJson object
def geojson_to_map_obj(df, one_feature, folium_obj, color_var, fill_op):
    """
    Adds a GeoJson object to the folium_map
    :param df: geopandas DataFrame that contains geometry for each shapely object and a column called 'feature_type'
    :param one_feature: type of feature
    :param folium_obj: folium map or feature group
    :param color_var: color of the GeoJson object
    :param fill_op: opacity of the GeoJson object
    :return:
    """
    if one_feature == 'central park':
        fill_op = 0
    gen_stylefunc = lambda x: {'color': color_var, 'fillOpacity': fill_op}
    to_geojson = folium.GeoJson(
        df[df['feature_type'] == one_feature],
        name=one_feature,
        style_function=gen_stylefunc)
    to_geojson.add_to(folium_obj)
    return


# b) FeatureGroup object
def featuregroup_to_map(df, one_feature, folium_map, color_var, fill_op):
    """
    Adds a FeatureGroup object to the folium_map.
    More versatile than a GeoJson object because you can keep adding things
    into the FeatureGroup and treat it as one layer
    :param df: geopandas DataFrame that contains geometry for each shapely object
    :param one_feature: type of feature
    :param folium_map: folium map
    :param color_var: color of the object
    :param fill_op: opacity of the object
    :return:
    """
    featuregroup = folium.FeatureGroup(name=one_feature)
    geojson_to_map_obj(df, one_feature, featuregroup, color_var, fill_op)
    featuregroup.add_to(folium_map)
    return featuregroup


# 2) MAP RAW DATA


raw_data_map = folium.Map(
    location=[40.7823, -73.96600],
    zoom_start=14,
    min_zoom=14,
    tiles='cartodbpositron',
    control_scale=True)

all_squirrels = folium.FeatureGroup(name="squirrels")

nyc_gdf = nyc_gdf.set_crs('epsg:4326')

for i in range(len(nyc_gdf)):
    folium.Circle(
        location=(nyc_gdf.iloc[i]['lat'], nyc_gdf.iloc[i]['long']),
        radius=2,
        tooltip=Tooltip('<p>' + str(dict(nyc_gdf.iloc[i])).replace(',', '<br>') + '<p>')
    ).add_to(all_squirrels)

all_squirrels.add_to(raw_data_map)


# 3) MAP FEATURES


# a) all features


cp_allfeaturesmap = folium.Map(
    location=[40.7823, -73.96600],
    zoom_start=14,
    min_zoom=14,
    tiles='cartodbpositron',
    control_scale=True
)

all_features = list(cp_allfeatures['feature_type'].unique())
all_colors = {'building': '#ad6f03',
              'garden': '#ff8cec',
              'grass': '#86b35d',
              'pedestrian': '#000000',
              'water': '#1795e8',
              'stream': '#1795e8',
              'woods': '#098f57',
              'paved': '#000000',
              'baseball': '#e0cdb4',
              'playground': '#f5931b',
              'sports center': '#960000',
              'bare rock': '#525252',
              'toilet': '#103b91',
              'central park': '#000000'}

for feature in all_features:
    geojson_to_map_obj(
        cp_allfeatures,
        feature,
        cp_allfeaturesmap,
        all_colors[feature],
        0.6
    )

folium.LayerControl().add_to(cp_allfeaturesmap)


# b) relevant features


cp_featuresmap = folium.Map(
    location=[40.7823, -73.96600],
    zoom_start=14,
    min_zoom=14,
    tiles='cartodbpositron',
    control_scale=True
)

for relev_feature in relev_features:
    geojson_to_map_obj(
        cp_features,
        relev_feature,
        cp_featuresmap,
        all_colors[relev_feature],
        0.6
    )

folium.LayerControl().add_to(cp_featuresmap)


# 4) MAP BUFFERS


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


# 5) MAP SQUIRRELS INSIDE BUFFER


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


