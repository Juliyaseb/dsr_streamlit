

import streamlit as st
import pandas as pd

# Dataset URL
data_url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    return df

df = load_data()

tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])


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
    st.subheader("Explore the Dataset")

    # Show full dataset
    st.dataframe(df, use_container_width=True)

    # Country filter
    countries = st.multiselect(
        "Select countries",
        options=sorted(df["country"].unique()),
        default=sorted(df["country"].unique())[:5]
    )

    # Year range slider
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    year_range = st.slider(
        "Select year range",
        min_year,
        max_year,
        (min_year, max_year)
    )

    # Filter data
    filtered_df = df[
        (df["country"].isin(countries)) &
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df, use_container_width=True)

    # Download filtered data
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        "Download filtered data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )