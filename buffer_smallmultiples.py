import pandas as pd
import plotly.express as px

from buffer_analysis import calculate_buffer_radius, buffer_analysis, geospatial_analysis
from data_cleaning import nyc_gdf1, behaviors, cp_features


def gen_small_multiples(arb_planar_features, exponent, constant_start, constant_end):
    buffersizecomp = pd.DataFrame(
        columns=['factor'] + geospatial_analysis
    )
    for constant in range(constant_start, constant_end, 1):
        arb_planar_features['buffer_radius'] = arb_planar_features['area'].apply(
            calculate_buffer_radius, power=exponent/10, factor=constant/10, cap=150, base=50
        )
        arb_buffer_features = buffer_analysis(nyc_gdf1, arb_planar_features)
        buffered_nyc_df = nyc_gdf1[['long', 'lat', 'geometry'] + behaviors + geospatial_analysis].to_crs('epsg:4326')
        bfsqrls = buffered_nyc_df.query('nearbuilding == True '
                                        'or neargarden == True '
                                        'or neargrass == True '
                                        'or nearpedestrian == True '
                                        'or nearwater == True '
                                        'or nearwoods == True'
                                        ).reset_index().drop(columns='index')
        add_one_row = bfsqrls[geospatial_analysis].sum()
        factor = pd.Series(data=constant/10, index=['factor'])
        one_row = pd.concat([factor, add_one_row])
        one_row_df = pd.DataFrame(one_row)
        buffersizecomp = pd.concat([buffersizecomp, one_row_df.transpose()], axis=0, ignore_index=True)
        print(constant/10)
    buffercomp = px.line(
        buffersizecomp,
        x='factor',
        y=buffersizecomp.columns[1:7],
        color_discrete_map={
            'nearbuilding': '#ad6f03',
            'neargarden': '#ff8cec',
            'neargrass': '#86b35d',
            'nearpedestrian': '#000000',
            'nearwater': '#1795e8',
            'nearwoods': '#098f57'
        },
        labels={
            'value': 'number of squirrels',
            'variable': 'buffer key'
        }
    )
    buffercomp.update_layout(
        title=dict(
            text='Squirrel Count for [factor * buffer area ^ ' + str(exponent/10) + ']',
            font=dict(
                size=10
            )
        ),
        legend=dict(
            font=dict(
                size=8
            )
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=False
        ),
        margin=dict(
            t=50,
            l=50,
            r=20,
            b=20
        ),
        font=dict(size=8)
    )
    buffercomp.write_html(
        'bufferradiuscomparison/buffer{0}.html'.format(str(exponent/10)),
    )


var_planar_features = cp_features.to_crs('epsg:2263')
var_planar_features['area'] = var_planar_features.geometry.area

for exponent in range(1, 6, 1):
    gen_small_multiples(var_planar_features, exponent, 1, 31)
