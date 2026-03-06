
import plotly.express as px
import streamlit as st
import pandas as pd
from model import train_model
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# Dataset URL
data_url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    return df

df = load_data()

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

features = [
    "gdp_per_capita",
    "headcount_ratio_upper_mid_income_povline",
    "year"
]

target = "life_expectancy_(ihme)"

X = df[features]
y = df[target]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

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

    # Year slider
    year = st.slider(
        "Select Year",
        int(df["year"].min()),
        int(df["year"].max()),
        int(df["year"].max())
    )

    # Filter dataset
    df_year = df[df["year"] == year]

    # Calculate metrics
    mean_life_exp = df_year["life_expectancy_(ihme)"].mean()
    median_gdp = df_year["gdp_per_capita"].median()
    mean_poverty = df_year["headcount_ratio_upper_mid_income_povline"].mean()
    num_countries = df_year["country"].nunique()

    # Create 4 columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Mean Life Expectancy",
            f"{mean_life_exp:.2f}"
        )

    with col2:
        st.metric(
            "Median GDP per Capita",
            f"{median_gdp:.2f}"
        )

    with col3:
        st.metric(
            "Mean Poverty Rate",
            f"{mean_poverty:.2f}"
        )

    with col4:
        st.metric(
            "Number of Countries",
            num_countries
        )
    
    fig = px.scatter(
        df_year,
        x="gdp_per_capita",
        y="life_expectancy_(ihme)",
        hover_name="country",
        size="gdp_per_capita",
        color="country",
        log_x=True,
        title="GDP per Capita vs Life Expectancy",
        labels={
            "gdp_per_capita": "GDP per Capita",
            "life_expectancy": "Life Expectancy (IHME)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Predict Life Expectancy")

    colA, colB, colC = st.columns(3)

    with colA:
        gdp_input = st.number_input(
            "GDP per capita",
            float(df["gdp_per_capita"].min()),
            float(df["gdp_per_capita"].max()),
            float(df["gdp_per_capita"].median())
        )

    with colB:
        poverty_input = st.number_input(
            "Poverty Rate",
            float(df["headcount_ratio_upper_mid_income_povline"].min()),
            float(df["headcount_ratio_upper_mid_income_povline"].max()),
            float(df["headcount_ratio_upper_mid_income_povline"].median())
        )

    with colC:
        year_input = st.slider(
            "Year",
            int(df["year"].min()),
            int(df["year"].max()),
            int(df["year"].median())
        )

    input_df = pd.DataFrame({
        "gdp_per_capita": [gdp_input],
        "headcount_ratio_upper_mid_income_povline": [poverty_input],
        "year": [year_input]
    })

    prediction = model.predict(input_df)[0]

    st.success(f"Predicted Life Expectancy: {prediction:.2f} years")

    # Feature importance
    importance_df = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    })

    fig_imp = px.bar(
        importance_df,
        x="feature",
        y="importance",
        title="Feature Importance"
    )

    st.plotly_chart(fig_imp, use_container_width=True)

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