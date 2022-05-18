import pandas as pd
import streamlit as st
import plotly.express as px


def app():
    st.title("Discussion of Results")

    st.markdown(
        """
        Here is a table of the p-values for all the combinations we conducted a permutation test on.
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
        st.plotly_chart(alluvial)
        st.markdown(
            """
            The interactive alluvial chart above helps visualize which behavior and feature was most common 
            and most significant. Feel free to drag the unique values for each variable to see the specific combinations
            more clearly.
            """
        )

    st.subheader("Observations")
    st.markdown(
        """
        - The `indifferent` behavior was the most common behavior that had a significant result. 
            - 8 out of the 18 significant combinations (~44.4%) had `indifferent` as the behavior.
            - Among the indifferent combinations, 5 out of the 8 had `neargrass` as a feature.
            - The 4 most statistically significant combinations had the `indifferent` behavior and `neargrass` feature. 
        - The `nearwoods` feature was the most common feature that had a significant result.
            - 10 out of the 18 significant combinations (~55.6%) had `nearwoods` as one of the features.
        - The `neargrass` feature was the next most common feature that had a significant result.
            - 9 out of the 18 significant combinations (50%) had `neargrass` as one of the features.
        """
    )

