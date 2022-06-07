import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def app():
    st.title("Discussion of Results")

    st.markdown(
        """
        The graphic below on the left is a table of the p-values for all the combinations we conducted a permutation test on.
        The right graphic is an interactive alluvial chart that visualizes which behavior and feature was most 
        common and most significant. Feel free to drag the unique values for each variable to see the 
        specific combinations more clearly.
        """
    )

    results = pd.read_csv('dataframes/permutation_results.csv')
    results = results.drop(columns='Unnamed: 0')
    sig = results[results['p-value'] < 0.05]

    col1, col2 = st.columns(2)
    with col1:
        sorted_by_p = sig.sort_values(by='p-value')
        hide_dataframe_row_index = """
                            <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            </style>
                            """
        # st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        # st.dataframe(sorted_by_p)
        hide_table_row_index = """
                    <style>
                    tbody th {display:none}
                    .blank {display:none}
                    </style>
                    """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(sorted_by_p)

    with col2:
        alluvial = px.parallel_categories(
            sig,
            dimensions=['behavior', 'feature 1', 'feature 2'],
            color='p-value',
            color_continuous_scale=px.colors.sequential.Oryel_r,
        )
        st.write("##")
        st.plotly_chart(alluvial)

    # heat map

    def combine(f1, f2):
        return str(f1[4:]) + " & " + str(f2[4:])

    feature_combo = results.apply(lambda x: combine(x['feature 1'], x['feature 2']), axis=1)

    results['feature combination'] = feature_combo

    hmap_results = results[['behavior', 'feature combination', 'p-value']]
    hmap_nans = hmap_results['p-value'].apply(lambda x: np.nan if x > 0.05 else x)
    hmap_all = hmap_results[['behavior', 'feature combination']]
    hmap_all['p-value'] = hmap_nans

    fig = go.Figure(
        data=go.Heatmap(
            x=hmap_all['behavior'],
            y=hmap_all['feature combination'],
            z=hmap_all['p-value'],
        )
    )

    fig.update_layout(
        height=800,
        width=1000,
        plot_bgcolor='#efefef',
        font_size=12
    )

    fig.update_traces(
        colorbar={
            'title': {
                'text': 'p-values ≤ 0.05'
            }
        },
        colorscale=['#3ba0e3', '#cee2f2'],
        text=hmap_results['p-value'],
        texttemplate="%{text}",
        textfont={"size": 16},
        textfont_color='#000000',
        selector={'type': 'heatmap'}
    )

    fig.update_xaxes(
        tickson='boundaries',
        side='top',
        title_text='behavior',

    )

    fig.update_yaxes(
        tickson='boundaries',
        title_text='feature combination'
    )

    st.write("#")

    st.markdown(
        """
        Below is a heatmap of the p-values of all the combinations that we conducted permutation tests on.
        The colored cells indicate a combination that had a statistically significant result, meaning
        that the p-value was less than or equal to the p-value cutoff of 0.05. Darker cells indicate
        a more statistically significant result, as illustrated on the color bar on the right.
        """
    )

    st.plotly_chart(fig)

    st.subheader("Observations")
    st.markdown(
        """
        - The `indifferent` behavior was the most common behavior that had a significant result. 
            - 8 out of the 18 significant combinations (~44.4%) had `indifferent` as the behavior.
            - Among the indifferent combinations, 5 out of the 8 had `grass` as a feature.
            - The 4 most statistically significant combinations had the `indifferent` behavior and `grass` feature. 
        - The `woods` feature was the most common feature that had a significant result.
            - 10 out of the 18 significant combinations (~55.6%) had `woods` as one of the features.
        - The `grass` feature was the next most common feature that had a significant result.
            - 9 out of the 18 significant combinations (50%) had `grass` as one of the features.
        """
    )

