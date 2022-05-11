import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from buffer_analysis import geospatial_analysis


behaviors = [
    'approaches', 'indifferent', 'runs_from',
    'running', 'chasing', 'eating', 'foraging', 'climbing']


def app():
    st.title("Statistical Testing: Permutation Tests")

    col1, col2, col3 = st.columns(3)

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
        elif variables == 0:
            st.write("Please select two features")
        else:
            st.write("Oh no! You can only select two features.")

    st.text("draw map of selected squirrels for the above variables")
    st.text("show plot and p-value")
