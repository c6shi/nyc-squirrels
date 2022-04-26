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

# drop unnecessary columns

trash = ['lat_long', 'community_districts', 'borough_boundaries',
         'city_council_districts', 'police_precincts']
nyc_gdf2 = nyc_gdf1.drop(columns=trash)
print(nyc_gdf2.columns)

# load geojson datasets

centralpark_water_osm = gpd.read_file('geojson/water_cp.geojson')
centralpark_stream_osm = gpd.read_file('geojson/streams_cp.geojson')
centralpark_playg_osm = gpd.read_file('geojson/playgrounds_cp.geojson')
centralpark_paved_osm = gpd.read_file('geojson/paved.geojson')
centralpark_toilets_osm = gpd.read_file('geojson/toilets.geojson')
cp_northbd_osm = gpd.read_file('geojson/northbd.geojson')  # cp north
cp_jorbd_osm = gpd.read_file('geojson/jorbd.geojson')  # jacqueline kennedy onassis reservoir
cp_greatlawnbd_osm = gpd.read_file('geojson/greatlawnbd.geojson')  # great lawn
cp_ramblebd_osm = gpd.read_file('geojson/ramblebd.geojson')  # ramble
cp_southbd_osm = gpd.read_file('geojson/southbd.geojson')  # cp south
met_osm = gpd.read_file('geojson/met.geojson')  # the met
centralpark_gardens_osm = gpd.read_file('geojson/gardens_cp.geojson')
allwoodsosm = gpd.read_file('geojson/woods_cp.geojson')
cp_baseball_osm = gpd.read_file('geojson/baseballpitch.geojson')
cp_field_osm = gpd.read_file('geojson/field.geojson')
allbarerockosm = gpd.read_file('geojson/bare_rock.geojson')
cp_pedestrian_osm = gpd.read_file('geojson/pedestrian.geojson')
cp_sportscenter_osm = gpd.read_file('geojson/sportscenter.geojson')

# data cleaning

