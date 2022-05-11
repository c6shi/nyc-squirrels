import geopandas as gpd
import math
import pyproj
import numpy as np
from data_cleaning import (
    centralpark_perimeter,
    nyc_gdf1,
    cp_features,
    relev_features,
    behaviors
)

# 1) REMOVING SQUIRRELS OUTSIDE OF CENTRAL PARK


squirrel_inside = nyc_gdf1.within(centralpark_perimeter)
nyc_gdf1 = nyc_gdf1.assign(inside=squirrel_inside)
nyc_gdf1 = nyc_gdf1[nyc_gdf1.get('inside')==True]


# 2) DETERMINING BEST BUFFER


# a) find area of each polygon (area dependent buffer size)
planar_features = cp_features.to_crs('epsg:2263')
planar_features['area'] = planar_features.geometry.area


# b) define buffer function (variable)
def calculate_buffer_radius(area, power, factor, cap, base):
    # buffer_counter[0] = factor
    if area == 0:
        return base
    math_func = math.pow(area, power) * factor
    if math_func > cap:
        return cap
    return math_func


# c) configure to projection crs
planar_crs = pyproj.CRS('epsg:2263')
geo_crs = pyproj.CRS('epsg:4326')
project = pyproj.Transformer.from_crs(
    geo_crs, planar_crs, always_xy=True).transform

geospatial_analysis = ['nearbuilding',
                       'neargarden',
                       'neargrass',
                       'nearpedestrian',
                       'nearwater',
                       'nearwoods']

# for i in range(1, 40, 1):
# factor = i/10
# buffer_counter = [0]

# d) apply buffer function
planar_features['buffer_radius'] = planar_features['area'].apply(
    calculate_buffer_radius, power=0.4, factor=1.2, cap=150, base=50)


# e) define buffer analysis function on planar projected points_df
# for each polygon in relevant features
def buffer_analysis(points_df):
    """
    Modifies points_df to include boolean values of whether the point is in the buffer
    :param points_df: dataframe with the points to buffer
    :return: a dataframe of buffer radius and buffer geometry for each polygon
    """
    buffer_geoseries = np.array([])

    for i in range(len(relev_features)):
        temp = planar_features[planar_features['feature_type'] == relev_features[i]].reset_index()
        temp_array = np.array([])

        for j in range(len(temp)):
            temp_array = np.append(temp_array, temp.geometry[j].buffer(temp['buffer_radius'][j]))

        buffer_geoseries = np.append(buffer_geoseries, temp_array)
        buffer_gpd = gpd.GeoDataFrame(geometry=buffer_geoseries)
        temp_gpd = gpd.GeoDataFrame(geometry=temp_array)
        temp_planar_buffer = temp_gpd.geometry.unary_union
        # creating buffer columns
        points_df[geospatial_analysis[i]] = points_df.to_crs('epsg:2263').within(temp_planar_buffer)

    planar_features['buffer_geometry'] = buffer_gpd.geometry

    return planar_features.set_geometry('buffer_geometry').drop(columns='geometry').to_crs('epsg:4326')


# f) create buffer_features for mapping specific buffers
buffer_features = buffer_analysis(nyc_gdf1)


# 3) BUFFERED DATASET PREPARED FOR PERMUTATION TESTS


buffered_nyc_df = nyc_gdf1[['long', 'lat', 'geometry'] + behaviors + geospatial_analysis].to_crs('epsg:4326')

bfsqrls = buffered_nyc_df.query('nearbuilding == True '
                                'or neargarden == True '
                                'or neargrass == True '
                                'or nearpedestrian == True '
                                'or nearwater == True '
                                'or nearwoods == True'
                                ).reset_index().drop(columns='index')

bfsqrls.to_csv('dataframes/bfsqrls.csv')
bfsqrlspd = bfsqrls.drop(columns=['long', 'lat', 'geometry'])
bfsqrlspd.to_csv('dataframes/bfsqrlspd.csv')

print(nyc_gdf1['approaches'].unique())
