import streamlit as st
from streamlit_folium import folium_static
from mapping import raw_data_map
from PIL import Image


def app():
    st.title("Data Analysis on Squirrels in Central Park, NYC")

    squirrel = Image.open('squirrel.jpg')
    st.image(squirrel)

    st.markdown(
        """
        In October 2018, a group of volunteers went out to Central Park to attempt 
        to record squirrel sightings. 
        """
    )

    st.subheader("Question: How do the different geographic features of Central Park affect squirrel's behaviors?")

    st.markdown(
        """
        Since we had access to geospatial data in the form of the coordinates of a squirrel sighting, 
        we wanted to make use of this information. Given the diverse environment of Central Park, 
        we decided to compare the geographic features of Central Park, 
        such as the water bodies, woods, open grassy areas, and more, with the behaviors recorded for each squirrel. 
        """
    )

    st.subheader("The Data Set")
    st.markdown(
        """
        Below is a map of all squirrels recorded in the 2018 Central Park Squirrel Census, 
        which can be downloaded from [NYC OpenData](https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw).
        [The Squirrel Census](https://www.thesquirrelcensus.com/about) 
        is an organization that conducts squirrel counts and presents their findings in fun ways. 
        According to The Squirrel Census, the purpose of this data collection is:
        - “to learn more about the populations and behaviors of the Eastern gray (which is so common that it’s often overlooked in academic studies);”
        - “to tell a data-driven narrative about Central Park and urban green spaces in general;”
        - “to engage in citizen science and community building;”
        - “to transform the space of Central Park into an art project and story that unfolded in real time.”
        With the help of volunteers, university and state departments, the Squirrel Census recorded 
        over 3,000 squirrel sightings. However, in their final report, they concluded that there were 
        exactly 2,373 squirrels in Central Park after “applying a formula from a 1959 squirrel study 
        to account for repeat sightings” [NYTimes article written by a volunteer](https://www.nytimes.com/interactive/2020/01/08/nyregion/central-park-squirrel-census.html). 
        Since we did not know how the formula worked and which squirrels were repeated, 
        we worked with the original raw data that contained 3,024 squirrels.
        """
    )

    folium_static(raw_data_map, width=620, height=680)

    st.markdown(
        """
        #### Rundown of the process
        
        1. getting outside data
        2. performing geospatial analysis/buffer analysis
        3. conducting permutation tests (our null hypothesis is...)
        """
    )
