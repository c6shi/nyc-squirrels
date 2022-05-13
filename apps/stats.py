import streamlit as st
import pandas as pd
import folium
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
from buffer_analysis import bfsqrls


behaviors = [
    'approaches', 'indifferent', 'runs_from',
    'running', 'chasing', 'eating', 'foraging', 'climbing']


permutation_results = pd.read_csv('dataframes/permutation_results.csv')
permutation_results = permutation_results.drop(columns='Unnamed: 0')


def app():
    st.title("Statistical Testing: Permutation Tests")

    st.markdown(
        """
        At this stage, we will be simulating permutation tests! In our simulation,
        we ran each unique combination of a certain behavior and two features 10,000 times.
        
        Put simply, this means we are testing to see if the observed difference in 
        the proportion of squirrels near one feature and that of squirrels near a 
        different feature is significantly different. A permutation test is a great option
        because it randomly shuffles the true/false values of a behavior among the certain
        pairs of features. 
        
        However, there arises the issue of overlapping features. Perhaps a squirrel
        can be located inside both features' buffers. We resolved this by ... 
        (try k-nearest neighbor algorithm and assign squirrel based on nearest group)
        
        To reduce runtime, the widget below is not running the permutation test
        live. 
        """
    )

    col1, col2 = st.columns(2)

    f1 = ''
    f2 = ''

    with col1:
        b = st.selectbox("Choose a behavior", behaviors)

    with col2:
        st.write("Choose the buffered features")
        building = st.checkbox("near building")
        garden = st.checkbox("near garden")
        grass = st.checkbox("near grass")
        pedestrian = st.checkbox("near pedestrian designated path")
        water = st.checkbox("near water")
        woods = st.checkbox("near woods")
        variables = building + garden + grass + pedestrian + water + woods

        if variables == 1:
            st.write("Please select one more feature")
        elif variables == 2:
            st.write("Awesome! Here's what that looks like:")
            if building:
                f1 = 'nearbuilding'
            if garden:
                if f1 == '':
                    f1 = 'neargarden'
                else:
                    f2 = 'neargarden'
            if grass:
                if f1 == '':
                    f1 = 'neargrass'
                else:
                    f2 = 'neargrass'
            if pedestrian:
                if f1 == '':
                    f1 = 'nearpedestrian'
                else:
                    f2 = 'nearpedestrian'
            if water:
                if f1 == '':
                    f1 = 'nearwater'
                else:
                    f2 = 'nearwater'
            if woods:
                if f1 == '':
                    f1 = 'nearwoods'
                else:
                    f2 = 'nearwoods'

            p = permutation_results[
                (permutation_results['behavior'] == b) &
                (permutation_results['feature 1'] == f1) &
                (permutation_results['feature 2'] == f2)
                ].get('p-value').array[0] * 100
        elif variables == 0:
            st.write("Please select two features")
        else:
            st.write("Oh no! You can only select two features.")

    st.text("draw map of selected squirrels for the above variables")

    if f1 != '' and f2 != '':
        st.subheader("Given that location does not affect behavior, {0} % of ".format(p) +
                     "our simulations showed a difference in proportion of squirrels doing "
                     "the {0} behavior near {1} and {2}".format(b, f1[4:], f2[4:], p))
        st.image('histograms/{0}/{1}_{2}.png'.format(b, f1, f2))
        st.subheader("p-value: {}".format(p))

        st.subheader("map")

        u_comb = folium.Map(
            location=[40.7823, -73.96600],
            zoom_start=14,
            min_zoom=14,
            tiles='cartodbpositron',
            control_scale=True)

        u_comb_squirrels = folium.FeatureGroup()

        u_comb_df = bfsqrls[(bfsqrls[f1]==True) | (bfsqrls[f2]==True)]

        for i in range(len(u_comb_df)):
            if u_comb_df.iloc[i][b] == True:
                color = '#FF4B4B'
            else:
                color = 'gray'
            folium.Circle(
                location=(u_comb_df.iloc[i]['lat'], u_comb_df.iloc[i]['long']),
                color=color,
                radius=2).add_to(u_comb_squirrels)

        u_comb_squirrels.add_to(u_comb)

        folium_static(u_comb, width=620, height=680)

    if st.checkbox("hit me with all the p-values!"):
        sorted_by_p = permutation_results.sort_values(by='p-value')
        st.dataframe(sorted_by_p)
