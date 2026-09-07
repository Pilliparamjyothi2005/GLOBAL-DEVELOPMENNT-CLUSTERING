import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Global Development Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Development Dashboard")
st.write("Compare development indicators between two countries.")

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

try:
   df = pd.read_excel("World_development_mesurement.xlsx")
except Exception as e:
    st.error("❌ Could not load the Excel file.")
    st.error(f"Error: {e}")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# --------------------------------------------------
# COUNTRY LIST
# --------------------------------------------------

if "Country" not in df.columns:
    st.error("❌ The dataset does not contain a 'Country' column.")
    st.stop()

countries = sorted(
    df["Country"].dropna().astype(str).unique()
)

if len(countries) < 2:
    st.error("❌ At least two countries are required.")
    st.stop()

# --------------------------------------------------
# COUNTRY SELECTION
# --------------------------------------------------

st.subheader("🌎 Select Two Countries for Comparison")

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

# Get country data
data1 = df[df["Country"].astype(str) == country1]
data2 = df[df["Country"].astype(str) == country2]

if data1.empty or data2.empty:
    st.error("❌ Country data could not be found.")
    st.stop()

# Take first row if multiple rows exist
country_data1 = data1.iloc[0]
country_data2 = data2.iloc[0]

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def convert_value(value):
    """Convert dataset values into numbers safely."""

    if pd.isna(value):
        return None

    if isinstance(value, str):

        value = (
            value.replace("$", "")
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
    """Format values for display."""

    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        return f"{value:,.2f}"

    return str(value)


# --------------------------------------------------
# BASIC COUNTRY DETAILS
# --------------------------------------------------

st.header("📊 Country Comparison")

col1, col2 = st.columns(2)

with col1:

    st.subheader(f"🌍 {country1}")

    if "GDP" in df.columns:
        st.metric(
            "GDP",
            display_value(country_data1["GDP"])
        )

    if "Population Total" in df.columns:
        st.metric(
            "Population",
            display_value(country_data1["Population Total"])
        )

    if "Internet Usage" in df.columns:
        st.metric(
            "Internet Usage",
            display_value(country_data1["Internet Usage"])
        )

    if "Life Expectancy Male" in df.columns:
        st.metric(
            "Life Expectancy Male",
            display_value(country_data1["Life Expectancy Male"])
        )

    if "Life Expectancy Female" in df.columns:
        st.metric(
            "Life Expectancy Female",
            display_value(country_data1["Life Expectancy Female"])
        )


with col2:

    st.subheader(f"🌍 {country2}")

    if "GDP" in df.columns:
        st.metric(
            "GDP",
            display_value(country_data2["GDP"])
        )

    if "Population Total" in df.columns:
        st.metric(
            "Population",
            display_value(country_data2["Population Total"])
        )

    if "Internet Usage" in df.columns:
        st.metric(
            "Internet Usage",
            display_value(country_data2["Internet Usage"])
        )

    if "Life Expectancy Male" in df.columns:
        st.metric(
            "Life Expectancy Male",
            display_value(country_data2["Life Expectancy Male"])
        )

    if "Life Expectancy Female" in df.columns:
        st.metric(
            "Life Expectancy Female",
            display_value(country_data2["Life Expectancy Female"])
        )


# --------------------------------------------------
# CATEGORIES
# --------------------------------------------------

categories = {

    "Population": [
        "Population 0-14",
        "Population 15-64",
        "Population 65+",
        "Population Total",
        "Population Urban"
    ],

    "Health": [
        "Health Exp % GDP",
        "Health Exp/Capita",
        "Life Expectancy Female",
        "Life Expectancy Male",
        "Infant Mortality Rate"
    ],

    "Economy": [
        "GDP",
        "Business Tax Rate",
        "Ease of Business",
        "Days to Start Business",
        "Hours to do Tax",
        "Lending Interest"
    ],

    "Technology": [
        "Internet Usage",
        "Mobile Phone Usage"
    ],

    "Environment": [
        "CO2 Emissions",
        "Energy Usage",
        "Birth Rate"
    ],

    "Tourism": [
        "Tourism Inbound",
        "Tourism Outbound"
    ]
}

# --------------------------------------------------
# CATEGORY SELECTION
# --------------------------------------------------

category = st.selectbox(
    "📂 Select Category",
    list(categories.keys())
)

# Only use columns that actually exist
available_cols = [
    col for col in categories[category]
    if col in df.columns
]

missing_cols = [
    col for col in categories[category]
    if col not in df.columns
]

if missing_cols:
    st.warning(
        "⚠️ Some indicators are not available in the dataset: "
        + ", ".join(missing_cols)
    )

if not available_cols:
    st.error("❌ No indicators are available for this category.")
    st.stop()

st.header(f"📈 {category} Comparison")

# --------------------------------------------------
# CREATE COMPARISON DATA
# --------------------------------------------------

values1 = []
values2 = []

for col in available_cols:

    values1.append(
        convert_value(country_data1[col])
    )

    values2.append(
        convert_value(country_data2[col])
    )

comparison_df = pd.DataFrame({

    "Indicator": available_cols,

    country1: values1,

    country2: values2

})

# --------------------------------------------------
# DISPLAY TABLE
# --------------------------------------------------

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

st.subheader("📊 Visual Comparison")

chart_df = comparison_df.set_index("Indicator")

st.bar_chart(
    chart_df,
    use_container_width=True
)

# --------------------------------------------------
# HIGHEST VALUE COMPARISON
# --------------------------------------------------

st.subheader("🏆 Highest Value Comparison")

results = []

for i in range(len(available_cols)):

    indicator = available_cols[i]

    value1 = values1[i]
    value2 = values2[i]

    if value1 is None or value2 is None:

        winner = "N/A"

    elif value1 > value2:

        winner = country1

    elif value2 > value1:

        winner = country2

    else:

        winner = "Equal"

    results.append({

        "Indicator": indicator,

        country1: value1,

        country2: value2,

        "Highest Value": winner

    })

result_df = pd.DataFrame(results)

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

st.subheader("🏅 Final Comparison Result")

country1_wins = 0
country2_wins = 0
equal_count = 0

for i in range(len(available_cols)):

    value1 = values1[i]
    value2 = values2[i]

    if value1 is None or value2 is None:
        continue

    if value1 > value2:

        country1_wins += 1

    elif value2 > value1:

        country2_wins += 1

    else:

        equal_count += 1


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        f"🏆 {country1} Wins",
        country1_wins
    )

with col2:

    st.metric(
        f"🏆 {country2} Wins",
        country2_wins
    )

with col3:

    st.metric(
        "🤝 Equal",
        equal_count
    )


if country1_wins > country2_wins:

    st.success(
        f"🏆 {country1} has the highest value in more indicators!"
    )

elif country2_wins > country1_wins:

    st.success(
        f"🏆 {country2} has the highest value in more indicators!"
    )

else:

    st.info(
        "🤝 Both countries have an equal number of wins!"
    )

# --------------------------------------------------
# COUNTRY DETAILS
# --------------------------------------------------

st.subheader(f"📋 {country1} Details")

st.dataframe(
    data1,
    use_container_width=True,
    hide_index=True
)

st.subheader(f"📋 {country2} Details")

st.dataframe(
    data2,
    use_container_width=True,
    hide_index=True
)
