import streamlit as st


def app():
    st.title("Final Thoughts")

    st.subheader("Project Improvements")
    st.markdown(
        """
        Had we had more time, we would have …
        - chosen the best buffer size in a more scientific way
        - conduct permutation tests based on a one-sided null hypothesis to determine which of the two features had a greater proportion of squirrels exhibiting a behavior than the other feature
        - address the issue with a squirrel being in multiple buffers using the k-nearest neighbor algorithm to assign a squirrel to one feature based on its surroundings
        - predict squirrel behavior based on location with ML algorithms
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