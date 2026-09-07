
import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Global Development Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Development Dashboard")
st.write("Compare development indicators between two countries.")

# =========================================================
# LOAD DATASET
# =========================================================

# IMPORTANT:
# Put World_development_mesurement.csv in the SAME folder as app.py

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / r"C:\Users\LENOVO\Downloads\World_development_mesurement.xlsx"
if not FILE_PATH.exists():
    st.error("❌ Dataset file not found.")
    st.info(
        "Make sure World_development_mesurement.csv "
        "is in the same GitHub folder as app.py."
    )

    st.code("""
Your GitHub repository should contain:

app.py
requirements.txt
World_development_mesurement.csv
""")

    st.stop()

try:
    df = pd.read_csv("C:\Users\LENOVO\Downloads\World_development_mesurement.xlsx")

except Exception as e:
    st.error("❌ Could not read the CSV file.")
    st.error(f"Error: {e}")
    st.stop()

# =========================================================
# CLEAN DATA
# =========================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

if df.empty:
    st.error("❌ Dataset is empty.")
    st.stop()

if "Country" not in df.columns:
    st.error("❌ 'Country' column is missing.")
    st.write("Columns found:")
    st.write(list(df.columns))
    st.stop()

# =========================================================
# COUNTRY LIST
# =========================================================

countries = sorted(
    df["Country"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

if len(countries) < 2:
    st.error("❌ At least two countries are required.")
    st.stop()

# =========================================================
# SELECT TWO COUNTRIES
# =========================================================

st.header("🌎 Select Two Countries")

col1, col2 = st.columns(2)

with col1:
    country1 = st.selectbox(
        "Select First Country",
        countries,
        index=0
    )

with col2:
    country2 = st.selectbox(
        "Select Second Country",
        countries,
        index=1
    )

if country1 == country2:
    st.warning("⚠️ Please select two different countries.")

# =========================================================
# GET COUNTRY DATA
# =========================================================

data1 = df[
    df["Country"].astype(str).str.strip() == country1
]

data2 = df[
    df["Country"].astype(str).str.strip() == country2
]

if data1.empty or data2.empty:
    st.error("❌ Country data not available.")
    st.stop()

country_data1 = data1.iloc[0]
country_data2 = data2.iloc[0]

# =========================================================
# CONVERT VALUES
# =========================================================

def convert_value(value):

    if pd.isna(value):
        return None

    if isinstance(value, str):

        value = (
            value
            .replace("$", "")
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        try:
            return float(value)

        except ValueError:
            return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


def display_value(value):

    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        return f"{value:,.2f}"

    return str(value)


# =========================================================
# BASIC COUNTRY INFORMATION
# =========================================================

st.header("📊 Country Comparison")

col1, col2 = st.columns(2)

with col1:

    st.subheader(f"🌍 {country1}")

    for indicator in [
        "GDP",
        "Population Total",
        "Internet Usage",
        "Life Expectancy Male",
        "Life Expectancy Female"
    ]:

        if indicator in df.columns:

            st.metric(
                indicator,
                display_value(country_data1[indicator])
            )


with col2:

    st.subheader(f"🌍 {country2}")

    for indicator in [
        "GDP",
        "Population Total",
        "Internet Usage",
        "Life Expectancy Male",
        "Life Expectancy Female"
    ]:

        if indicator in df.columns:

            st.metric(
                indicator,
                display_value(country_data2[indicator])
            )


# =========================================================
# DEVELOPMENT CLUSTERS
# =========================================================

clusters = {

    "Cluster 1 - Social Development": [
        "Population 0-14",
        "Population 15-64",
        "Population 65+",
        "Population Total",
        "Population Urban",
        "Life Expectancy Female",
        "Life Expectancy Male",
        "Infant Mortality Rate"
    ],

    "Cluster 2 - Economic & Technology Development": [
        "GDP",
        "Business Tax Rate",
        "Ease of Business",
        "Days to Start Business",
        "Hours to do Tax",
        "Lending Interest",
        "Internet Usage",
        "Mobile Phone Usage",
        "Health Exp % GDP",
        "Health Exp/Capita"
    ],

    "Cluster 3 - Environment & Tourism": [
        "CO2 Emissions",
        "Energy Usage",
        "Birth Rate",
        "Tourism Inbound",
        "Tourism Outbound"
    ]
}

# =========================================================
# CLUSTER SELECTION
# =========================================================

st.header("🔬 Development Cluster Comparison")

cluster1, cluster2 = st.columns(2)

with cluster1:

    selected_cluster1 = st.selectbox(
        "Select First Cluster",
        list(clusters.keys()),
        index=0
    )

with cluster2:

    selected_cluster2 = st.selectbox(
        "Select Second Cluster",
        list(clusters.keys()),
        index=1
    )


# =========================================================
# FUNCTION TO CREATE CLUSTER TABLE
# =========================================================

def create_cluster_table(cluster_name):

    indicators = [
        indicator
        for indicator in clusters[cluster_name]
        if indicator in df.columns
    ]

    rows = []

    for indicator in indicators:

        value1 = convert_value(country_data1[indicator])
        value2 = convert_value(country_data2[indicator])

        if value1 is None or value2 is None:
            winner = "N/A"

        elif value1 > value2:
            winner = country1

        elif value2 > value1:
            winner = country2

        else:
            winner = "Equal"

        rows.append({
            "Indicator": indicator,
            country1: value1,
            country2: value2,
            "Higher Value": winner
        })

    return pd.DataFrame(rows)


# =========================================================
# CLUSTER 1 COMPARISON
# =========================================================

st.subheader(f"📈 {selected_cluster1}")

cluster_df1 = create_cluster_table(selected_cluster1)

if cluster_df1.empty:

    st.warning("⚠️ No indicators available for this cluster.")

else:

    st.dataframe(
        cluster_df1,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CLUSTER 2 COMPARISON
# =========================================================

st.subheader(f"📈 {selected_cluster2}")

cluster_df2 = create_cluster_table(selected_cluster2)

if cluster_df2.empty:

    st.warning("⚠️ No indicators available for this cluster.")

else:

    st.dataframe(
        cluster_df2,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# VISUAL COMPARISON
# =========================================================

st.header("📊 Visual Comparison")

if not cluster_df1.empty:

    chart_data = cluster_df1.set_index("Indicator")[
        [country1, country2]
    ]

    st.bar_chart(
        chart_data,
        use_container_width=True
    )


# =========================================================
# CLUSTER WINNER FUNCTION
# =========================================================

def calculate_wins(cluster_df):

    country1_wins = 0
    country2_wins = 0
    equal = 0

    for _, row in cluster_df.iterrows():

        value1 = row[country1]
        value2 = row[country2]

        if pd.isna(value1) or pd.isna(value2):
            continue

        if value1 > value2:
            country1_wins += 1

        elif value2 > value1:
            country2_wins += 1

        else:
            equal += 1

    return country1_wins, country2_wins, equal


# =========================================================
# CLUSTER RESULTS
# =========================================================

st.header("🏆 Cluster Results")

if not cluster_df1.empty:

    wins1, wins2, equal1 = calculate_wins(cluster_df1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"{country1} Wins",
            wins1
        )

    with col2:
        st.metric(
            f"{country2} Wins",
            wins2
        )

    with col3:
        st.metric(
            "Equal",
            equal1
        )

    if wins1 > wins2:

        st.success(
            f"🏆 {country1} performs higher in more "
            f"indicators in {selected_cluster1}."
        )

    elif wins2 > wins1:

        st.success(
            f"🏆 {country2} performs higher in more "
            f"indicators in {selected_cluster1}."
        )

    else:

        st.info(
            "🤝 Both countries have the same number of wins."
        )


# =========================================================
# FINAL TWO-CLUSTER COMPARISON
# =========================================================

st.header("🎯 Final Two-Cluster Comparison")

if not cluster_df1.empty and not cluster_df2.empty:

    c1_wins_1, c2_wins_1, equal_1 = calculate_wins(cluster_df1)

    c1_wins_2, c2_wins_2, equal_2 = calculate_wins(cluster_df2)

    total_country1 = c1_wins_1 + c1_wins_2
    total_country2 = c2_wins_1 + c2_wins_2
    total_equal = equal_1 + equal_2

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            f"🏆 {country1}",
            total_country1
        )

    with col2:

        st.metric(
            f"🏆 {country2}",
            total_country2
        )

    with col3:

        st.metric(
            "🤝 Equal",
            total_equal
        )

    if total_country1 > total_country2:

        st.success(
            f"🏆 Overall result: {country1} "
            f"has the higher value in more indicators "
            f"across the two selected clusters."
        )

    elif total_country2 > total_country1:

        st.success(
            f"🏆 Overall result: {country2} "
            f"has the higher value in more indicators "
            f"across the two selected clusters."
        )

    else:

        st.info(
            "🤝 Overall result: Both countries have "
            "the same number of higher indicators."
        )


# =========================================================
# FULL DATA
# =========================================================

with st.expander(f"📋 Show {country1} Full Data"):

    st.dataframe(
        data1,
        use_container_width=True,
        hide_index=True
    )


with st.expander(f"📋 Show {country2} Full Data"):

    st.dataframe(
        data2,
        use_container_width=True,
        hide_index=True
    )
