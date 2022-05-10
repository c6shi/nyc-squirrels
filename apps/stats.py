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
        f1 = st.selectbox("Choose a feature", geospatial_analysis)

    with col3:
        f2_options = geospatial_analysis
        f2 = st.selectbox("Choose another feature", f2_options)

    st.text("draw map of selected squirrels for the above variables")
    st.text("show plot and p-value")
