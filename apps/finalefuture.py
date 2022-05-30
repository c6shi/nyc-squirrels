import streamlit as st


def app():
    st.title("Final Thoughts")

    st.subheader("Project Improvements")
    st.markdown(
        """
        Had we had more time, we would have …
        - chosen the best buffer size in a more scientific way, which in itself is another data analysis question
        - conduct permutation tests based on a one-sided null hypothesis to determine which of the two features had a greater proportion of squirrels exhibiting a behavior than the other feature
        - address the issue with a squirrel being in multiple buffers using the k-nearest neighbor algorithm to assign a squirrel to one feature based on its surroundings
        - predict squirrel behavior based on location with ML algorithms
        
        In addition, it would have been interesting to see how different times of the year affected squirrel behavior, 
        and whether there is a general trend in squirrel behavior in future years. 
        """
    )

    st.subheader("Future Direction")
    st.markdown(
        """
        Ultimately, analyzing squirrel data, while seemingly inconsequential, 
        illustrates a change in the way we perceive not just the human world but 
        the natural as well–and how humans can impact that natural data. 
        Analyzing how different structures and aspects of a man-made park impact 
        squirrels represents an example of a growing interest in how humans are 
        impacting our world in ways we never did before, as data has become the 
        new powerful tool to find answers to this question. With the massive 
        amounts of data in today’s world, we have a viable approach to quantify 
        humanity’s impact on the world, whether positive or negative. 
        Essentially, data gives us the opportunity to self reflect on how our 
        choices affect the coinhabitants of this planet, including squirrels. 
        While working on this project, we were not necessarily able to approach 
        this wide of a scope, but we still learned a lot more about squirrels 
        and Central Park and hope our project sets an example for the possibilities 
        of what we can learn about ourselves and our fellow animals. 
        """
    )

    st.subheader("Current Events: Urban Ecology and Climate Change")
    st.markdown(
        """
        In January 2022, the Yale School of the Environment announced that they would
        be parterning with Central Park Conservancy and Natural Areas Conservancy to 
        help cities study the impacts of climate change on their urban parks. As the country
        continues to urbanize, urban parks will face the pressures of an increase in 
        population and the inevitable impacts of human-driven climate change. These include 
        severe weather events as we have seen in the recent years: hurricanes bringing 
        a sudden onset of rain and floods, followed by heat waves and droughts. These changes are 
        occurring too fast for the ecosystems in city parks to adapt, which results in 
        loss of species and the growing concerns and calls for action. Urban parks will also 
        continue to be one of the first experiences of nature for many urban people. These 
        kinds of studies, like the Central Park Climate Lab, will bring awareness to the 
        effects of climate change on nature, as well as the importance of these green spaces 
        in response to climate change.
        
        Why should you care? Urban parks are essential to the social well-being and resilience of
        a community, the physical and mental health of individuals, and the reduction of the
        heat island effect. There is no doubt that urban parks will be part of our future. 
        However, in times of financial crisis and ecological stress, we will need to become smarter and more 
        effective in the ways we design and use parks. Data analysis and data-driven solutions are the 
        key to working towards a more sustainable urban lifestyle and allowing for these spaces to 
        continue serving our communities. 
        
        Sources:
        - ["Protecting Our Urban Parks from the Impacts of Climate Change".](https://environment.yale.edu/news/article/protecting-our-urban-parks-impacts-climate-change) Yale School of the Envrionment, 12 Jan 2022.
        - ["The Central Park Climate Lab: Leading The Fight Against The Effects Of Climate Change On City Parks".](https://www.centralparknyc.org/press/climate-lab-leading-fight-against-climate-change-city-parks) Central Park Conservancy, 11 Jan 2022.
        - ["Putting people in the map: anthropogenic biomes of the world".](https://esajournals.onlinelibrary.wiley.com/doi/10.1890/070062) Frontiers in Ecology and the Environment, 1 Oct 2008.
        - ["Urbanization".](https://ourworldindata.org/urbanization) Our World in Data, 2018.
        - ["Why City Parks Matter".](https://cityparksalliance.org/about-us/why-city-parks-matter/) City Parks Alliance.
        - ["Room to Roam".](https://www.lincolninst.edu/publications/articles/2020-10-room-roam-pandemic-urban-parks-what-comes-next) Lincoln Institute of Land Policy, 7 Oct 2020.
        - ["Eastern Gray Squirrel".](https://oepos.ca.uky.edu/content/eastern-gray-squirrel) University of Kentucky College of Agriculture, Food and Environment.
        - ["Urban Ecology: the increasing importance of nature in the city".](https://www.tudelft.nl/en/stories/articles/urban-ecology-the-increasing-importance-of-nature-in-the-city) TU Delft.
        """
    )
