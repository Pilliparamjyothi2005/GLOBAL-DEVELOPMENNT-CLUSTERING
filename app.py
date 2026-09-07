```python
import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Global Development Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Development Dashboard")
st.write("Compare development indicators between two countries.")

# =========================================================
# LOAD EXCEL FILE
# =========================================================

BASE_DIR = Path(__file__).parent

FILE_PATH = BASE_DIR / "World_development_mesurement.xlsx"

if not FILE_PATH.exists():
    st.error("❌ Dataset file not found.")

    st.write("Your GitHub repository must contain:")

    st.code("""
app.py
requirements.txt
World_development_mesurement.xlsx
""")

    st.stop()

try:
    df = pd.read_excel(FILE_PATH)

except Exception as e:
    st.error("❌ Could not read the Excel file.")
    st.error(str(e))
    st.stop()

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

# =========================================================
# CHECK DATA
# =========================================================

if df.empty:
    st.error("❌ Dataset is empty.")
    st.stop()

if "Country" not in df.columns:
    st.error("❌ 'Country' column was not found.")

    st.write("Columns available in your dataset:")
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
    st.stop()

# =========================================================
# GET COUNTRY DATA
# =========================================================

data1 = df[
    df["Country"].astype(str).str.strip() == country1
]

data2 = df[
    df["Country"].astype(str).str.strip() == country2
]

if data1.empty:
    st.error(f"❌ No data found for {country1}.")
    st.stop()

if data2.empty:
    st.error(f"❌ No data found for {country2}.")
    st.stop()

country_data1 = data1.iloc[0]
country_data2 = data2.iloc[0]

# =========================================================
# CONVERT VALUES TO NUMBERS
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

        if value == "":
            return None

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

basic_indicators = [
    "GDP",
    "Population Total",
    "Internet Usage",
    "Life Expectancy Male",
    "Life Expectancy Female"
]

with col1:

    st.subheader(f"🌍 {country1}")

    for indicator in basic_indicators:

        if indicator in df.columns:

            st.metric(
                indicator,
                display_value(country_data1[indicator])
            )

with col2:

    st.subheader(f"🌍 {country2}")

    for indicator in basic_indicators:

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
# SELECT TWO CLUSTERS
# =========================================================

st.header("🔬 Development Cluster Comparison")

cluster_names = list(clusters.keys())

col1, col2 = st.columns(2)

with col1:

    selected_cluster1 = st.selectbox(
        "Select First Cluster",
        cluster_names,
        index=0
    )

with col2:

    selected_cluster2 = st.selectbox(
        "Select Second Cluster",
        cluster_names,
        index=1
    )

# =========================================================
# CREATE COMPARISON
# =========================================================

def create_comparison(cluster_name):

    indicators = []

    for indicator in clusters[cluster_name]:

        if indicator in df.columns:
            indicators.append(indicator)

    rows = []

    for indicator in indicators:

        value1 = convert_value(
            country_data1[indicator]
        )

        value2 = convert_value(
            country_data2[indicator]
        )

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
# FIRST CLUSTER
# =========================================================

st.subheader(f"📈 {selected_cluster1}")

cluster_df1 = create_comparison(
    selected_cluster1
)

if cluster_df1.empty:

    st.warning(
        "No indicators from this cluster "
        "were found in the dataset."
    )

else:

    st.dataframe(
        cluster_df1,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# SECOND CLUSTER
# =========================================================

st.subheader(f"📈 {selected_cluster2}")

cluster_df2 = create_comparison(
    selected_cluster2
)

if cluster_df2.empty:

    st.warning(
        "No indicators from this cluster "
        "were found in the dataset."
    )

else:

    st.dataframe(
        cluster_df2,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# CHART
# =========================================================

st.header("📊 Visual Comparison")

if not cluster_df1.empty:

    chart_data = cluster_df1.set_index(
        "Indicator"
    )[[country1, country2]]

    st.bar_chart(
        chart_data,
        use_container_width=True
    )

# =========================================================
# CALCULATE WINS
# =========================================================

def calculate_wins(comparison_df):

    country1_wins = 0
    country2_wins = 0
    equal_count = 0

    for _, row in comparison_df.iterrows():

        value1 = row[country1]
        value2 = row[country2]

        if pd.isna(value1) or pd.isna(value2):
            continue

        if value1 > value2:

            country1_wins += 1

        elif value2 > value1:

            country2_wins += 1

        else:

            equal_count += 1

    return (
        country1_wins,
        country2_wins,
        equal_count
    )

# =========================================================
# CLUSTER RESULTS
# =========================================================

st.header("🏆 Cluster Results")

total_country1 = 0
total_country2 = 0
total_equal = 0

if not cluster_df1.empty:

    w1, w2, e1 = calculate_wins(
        cluster_df1
    )

    total_country1 += w1
    total_country2 += w2
    total_equal += e1

    st.subheader(
        f"🏅 {selected_cluster1}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"🏆 {country1} Wins",
            w1
        )

    with col2:
        st.metric(
            f"🏆 {country2} Wins",
            w2
        )

    with col3:
        st.metric(
            "🤝 Equal",
            e1
        )

if not cluster_df2.empty:

    w1, w2, e1 = calculate_wins(
        cluster_df2
    )

    total_country1 += w1
    total_country2 += w2
    total_equal += e1

    st.subheader(
        f"🏅 {selected_cluster2}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"🏆 {country1} Wins",
            w1
        )

    with col2:
        st.metric(
            f"🏆 {country2} Wins",
            w2
        )

    with col3:
        st.metric(
            "🤝 Equal",
            e1
        )

# =========================================================
# FINAL RESULT
# =========================================================

st.header("🎯 Final Two-Cluster Result")

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
        f"🥇 Overall Winner: {country1}"
    )

elif total_country2 > total_country1:

    st.success(
        f"🥇 Overall Winner: {country2}"
    )

else:

    st.info(
        "🤝 Overall Result: Tie"
    )

# =========================================================
# FULL DATA
# =========================================================

st.header("📋 Full Country Data")

with st.expander(
    f"Show complete data for {country1}"
):

    st.dataframe(
        data1,
        use_container_width=True,
        hide_index=True
    )

with st.expander(
    f"Show complete data for {country2}"
):

    st.dataframe(
        data2,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🌍 Global Development Dashboard | "
    "Two Country & Two Cluster Comparison"
)
```

### `requirements.txt`

Because this version reads an **Excel `.xlsx` file**, your `requirements.txt` needs `openpyxl`:

```text
streamlit
pandas
openpyxl
```

### ⚠️ One important thing

You must upload **the actual Excel file** to GitHub:

```text
World_development_mesurement.xlsx
```

Do **not** use your computer path:

```text
C:\Users\LENOVO\Downloads\...
```

The current code you showed still contains that local path, which is the reason the error continues.

If your GitHub currently has **`World_development_mesurement.csv` instead of `.xlsx`**, tell me and I'll give you the exact CSV version.
