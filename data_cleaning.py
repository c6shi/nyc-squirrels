import pandas as pd
import geopandas as gpd
import numpy as np
import folium
import shapely
from shapely.ops import transform, Point, Polygon, nearest_points
from shapely.geometry import mapping

# 1) CLEANING GIVEN DATASET


# a) read data and transform to wgs84
nyc_gdf = gpd.read_file('dataframes/nycsquirrels_clean_1.csv')
nyc_gdf = gpd.GeoDataFrame(nyc_gdf, geometry=gpd.points_from_xy(nyc_gdf.long, nyc_gdf.lat))
nyc_gdf1 = nyc_gdf.set_crs('epsg:4326')

# b) convert fake bools (string) into 0s and 1s
behaviors = ['approaches', 'indifferent', 'runs_from',
             'running', 'chasing', 'climbing', 'eating', 'foraging',
             'kuks', 'quaas', 'moans', 'tail_flags', 'tail_twitches']

behavior_to_int = pd.DataFrame(
    {behavior: nyc_gdf1[behavior].apply(lambda x: 1 if x == 'TRUE' else 0) for behavior in behaviors})
nyc_gdf1.update(behavior_to_int)

# c) convert fake floats (string) to floats
long_float = nyc_gdf1['long'].apply(lambda x: float(x))
lat_float = nyc_gdf['lat'].apply(lambda x: float(x))

nyc_gdf1 = nyc_gdf1.assign(long=nyc_gdf1['long'].apply(lambda x: float(x)),
                           lat=nyc_gdf['lat'].apply(lambda x: float(x)))

# 2) ADDING OSM DATA


# a) load geojson datasets
centralpark = gpd.read_file('geojson/centralpark.geojson')
water_osm = gpd.read_file('geojson/water_cp.geojson')
stream_osm = gpd.read_file('geojson/streams_cp.geojson')
playg_osm = gpd.read_file('geojson/playgrounds_cp.geojson')
paved_osm = gpd.read_file('geojson/paved.geojson')
toilets_osm = gpd.read_file('geojson/toilets.geojson')
northbd_osm = gpd.read_file('geojson/northbd.geojson')  # cp north
jorbd_osm = gpd.read_file('geojson/jorbd.geojson')  # jacqueline kennedy onassis reservoir
greatlawnbd_osm = gpd.read_file('geojson/greatlawnbd.geojson')  # great lawn
ramblebd_osm = gpd.read_file('geojson/ramblebd.geojson')  # ramble
southbd_osm = gpd.read_file('geojson/southbd.geojson')  # cp south
met_osm = gpd.read_file('geojson/met.geojson')  # museums (MET and others outside)
gardens_osm = gpd.read_file('geojson/gardens_cp.geojson')
woods_osm = gpd.read_file('geojson/woods_cp.geojson')
baseball_osm = gpd.read_file('geojson/baseballpitch.geojson')
grass_osm = gpd.read_file('geojson/field.geojson')
barerock_osm = gpd.read_file('geojson/bare_rock.geojson')
pedestrian_osm = gpd.read_file('geojson/pedestrian.geojson')
sportscenter_osm = gpd.read_file('geojson/sportscenter.geojson')

# b) select for features in central park
centralpark = centralpark.take([1])
centralpark_perimeter = centralpark.unary_union.convex_hull


# c) fix invalid geometries
def fix_invalid(df, index):
    fixed = df.geometry[index].buffer(0)
    new_geom = df.geometry
    new_geom[index] = fixed
    df.geometry = new_geom


fix_invalid(woods_osm, 1)
fix_invalid(pedestrian_osm, 0)

# 3) SELECT ALL FEATURES WITHIN CENTRAL PARK


cp_water = water_osm[water_osm.within(centralpark_perimeter)].assign(feature_type='water')
cp_stream = stream_osm[stream_osm.within(centralpark_perimeter)].assign(feature_type='water')
cp_playg = playg_osm[playg_osm.within(centralpark_perimeter)].assign(feature_type='playground')
cp_paved = paved_osm[paved_osm.within(centralpark_perimeter)].assign(feature_type='paved')
cp_toilets = toilets_osm[toilets_osm.within(centralpark_perimeter)].assign(feature_type='toilet')
cp_building = pd.concat([northbd_osm[northbd_osm.within(centralpark_perimeter)],
                         jorbd_osm[jorbd_osm.within(centralpark_perimeter)],
                         greatlawnbd_osm[greatlawnbd_osm.within(centralpark_perimeter)],
                         ramblebd_osm[ramblebd_osm.within(centralpark_perimeter)],
                         southbd_osm[southbd_osm.within(centralpark_perimeter)],
                         met_osm[met_osm.within(centralpark_perimeter)]]).assign(feature_type='building')
cp_garden = gardens_osm[gardens_osm.within(centralpark_perimeter)].assign(feature_type='garden')
cp_woods = woods_osm[woods_osm.within(centralpark_perimeter)].assign(feature_type='woods')
cp_baseballpitch = baseball_osm[baseball_osm.within(centralpark_perimeter)].assign(feature_type='baseball')
cp_grass = grass_osm[grass_osm.within(centralpark_perimeter)].assign(feature_type='grass')
cp_barerock = barerock_osm[barerock_osm.within(centralpark_perimeter)].assign(feature_type='bare rock')
cp_pedestrian = pedestrian_osm[pedestrian_osm.within(centralpark_perimeter)].assign(feature_type='pedestrian')
cp_sportscenter = sportscenter_osm[sportscenter_osm.within(centralpark_perimeter)].assign(feature_type='sports center')

all_features = [cp_water,
                cp_stream,
                cp_playg,
                cp_paved,
                cp_toilets,
                cp_building,
                cp_garden,
                cp_woods,
                cp_baseballpitch,
                cp_grass,
                cp_barerock,
                cp_pedestrian,
                cp_sportscenter]

# 4) CONCATENATE AND SAVE AS ALL/RELEVANT FEATURES


cp_allfeatures = pd.concat(all_features)
cp_allfeatures = (
    cp_allfeatures[np.array(
        [not isinstance(geom_object, shapely.geometry.point.Point)
         for geom_object in cp_allfeatures.geometry])]
)[['id', 'geometry', 'name', 'feature_type']].reset_index().drop(columns='index')

relev_features = ['building', 'garden', 'grass', 'pedestrian', 'water', 'woods']

cp_allfeatures.replace({'feature_type': 'stream'}, 'water', inplace=True)
cp_features = (
    cp_allfeatures.query('feature_type in @relev_features')
                  .sort_values(by='feature_type')
                  .reset_index(drop=True))

cp_allfeatures.to_csv('dataframes/cp_allfeatures.csv')
cp_features.to_csv('dataframes/cp_features.csv')

# delete from here
cp_allfeaturesmap = folium.Map(location=[40.7823, -73.96600],
                               zoom_start=14,
                               min_zoom=14,
                               tiles='cartodbpositron',
                               control_scale=True)


def to_geojson_map(df, feature, folium_map, color_var, fillOp):
    gen_stylefunc = lambda x: {'color': color_var, 'fillOpacity': fillOp}
    to_geojson = folium.GeoJson(df[df['feature_type'] == feature],
                                name=feature,
                                style_function=gen_stylefunc)
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

cp_featuresmap = folium.Map(location=[40.7823, -73.96600],
                            zoom_start=14,
                            min_zoom=14,
                            tiles='cartodbpositron',
                            control_scale=True)

for i in range(len(relev_features)):
    to_geojson_map(cp_features, relev_features[i], cp_featuresmap, allcolors[relev_features[i]], 0.6)

folium.LayerControl().add_to(cp_featuresmap)
