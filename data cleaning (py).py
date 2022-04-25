import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import folium
import shapely
import pyproj
from shapely.ops import transform, Point, Polygon

# read data and transform to wgs84

nyc_gdf = gpd.read_file('nycsquirrels_clean_1.csv')
nyc_gdf = gpd.GeoDataFrame(nyc_gdf,
                           geometry=gpd.points_from_xy(nyc_gdf.long, nyc_gdf.lat))
nyc_gdf1 = nyc_gdf.set_crs('epsg:4326')

# convert fake bools (string) into 0s and 1s

behaviors = ['approaches', 'indifferent', 'runs_from',
             'running', 'chasing', 'climbing', 'eating', 'foraging',
             'kuks', 'quaas', 'moans', 'tail_flags', 'tail_twitches']

bool_to_int = lambda x: 1 if x == 'TRUE' else 0

behavior_to_int = pd.DataFrame({behavior: nyc_gdf1[behavior].apply(bool_to_int)
                                for behavior in behaviors})
nyc_gdf1.update(behavior_to_int)

# convert fake floats (string) to floats

long_float = nyc_gdf1['long'].apply(lambda x: float(x))
lat_float = nyc_gdf['lat'].apply(lambda x: float(x))

nyc_gdf1 = nyc_gdf1.assign(long=nyc_gdf1['long'].apply(lambda x: float(x)),
                           lat=nyc_gdf['lat'].apply(lambda x: float(x)))
print("hello")