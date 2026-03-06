import streamlit as st


# Use full width layout
st.set_page_config(layout="wide")

# Header
st.header("Worldwide Analysis of Quality of Life and Economic Factors")

# Subtitle
st.write(
    """
This app enables you to explore the relationships between poverty, 
life expectancy, and GDP across various countries and years. 
Use the panels to select options and interact with the data.
"""
)

# Create tabs
tab1, tab2, tab3 = st.tabs(
    ["Global Overview", "Country Deep Dive", "Data Explorer"]
)

# Tab 1
with tab1:
    st.subheader("Global Overview")
    st.write("Visualize global trends across countries.")

# Tab 2
with tab2:
    st.subheader("Country Deep Dive")
    st.write("Explore detailed data for a specific country.")

# Tab 3
with tab3:
    st.subheader("Data Explorer")
    st.write("Interact with the raw dataset.")