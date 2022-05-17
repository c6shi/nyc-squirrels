import pandas as pd
import streamlit as st
import plotly.express as px


def app():
    st.title("Discussion of Results")

    results = pd.read_csv('dataframes/permutation_results.csv')
    results = results.drop(columns='Unnamed: 0')

    sig = results[results['p-value'] < 0.05]
    alluvial = px.parallel_categories(
        sig,
        dimensions=['behavior', 'feature 1', 'feature 2'],
        color='p-value',
        color_continuous_scale=px.colors.sequential.Oryel_r,
        width=1000,
        height=600,
    )
    alluvial.update_layout(
        font=dict(size=20)
    )
    st.plotly_chart(alluvial)

