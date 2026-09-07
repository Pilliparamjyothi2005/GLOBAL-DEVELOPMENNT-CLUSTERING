import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Global Development Dashboard",
    layout="wide"
)

st.title("🌍 Global Development Dashboard")

# Load Dataset
df = pd.read_excel("World_development_mesurement.xlsx")

# Get country list
countries = sorted(df["Country"].dropna().unique())

# ---------------- COUNTRY SELECTION ----------------

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

# Country data
country_data1 = df[df["Country"] == country1].iloc[0]
country_data2 = df[df["Country"] == country2].iloc[0]

# ---------------- BASIC DETAILS ----------------

st.header("📊 Country Comparison")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🌍 {country1}")

    st.metric(
        "GDP",
        country_data1["GDP"]
    )

    st.metric(
        "Population",
        country_data1["Population Total"]
    )

    st.metric(
        "Internet Usage",
        country_data1["Internet Usage"]
    )

    st.metric(
        "Life Expectancy Male",
        country_data1["Life Expectancy Male"]
    )

    st.metric(
        "Life Expectancy Female",
        country_data1["Life Expectancy Female"]
    )

with col2:
    st.subheader(f"🌍 {country2}")

    st.metric(
        "GDP",
        country_data2["GDP"]
    )

    st.metric(
        "Population",
        country_data2["Population Total"]
    )

    st.metric(
        "Internet Usage",
        country_data2["Internet Usage"]
    )

    st.metric(
        "Life Expectancy Male",
        country_data2["Life Expectancy Male"]
    )

    st.metric(
        "Life Expectancy Female",
        country_data2["Life Expectancy Female"]
    )

# ---------------- CATEGORIES ----------------

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

# Select Category
category = st.selectbox(
    "Select Category",
    list(categories.keys())
)

cols = categories[category]

st.header(
    f"📈 {category} Comparison"
)

# ---------------- FUNCTION TO CONVERT VALUES ----------------

def convert_value(value):

    if pd.isna(value):
        return 0

    if isinstance(value, str):

        value = (
            value.replace("$", "")
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        try:
            return float(value)

        except:
            return 0

    return float(value)


# ---------------- CREATE DATA ----------------

values1 = []
values2 = []

for col in cols:

    values1.append(
        convert_value(country_data1[col])
    )

    values2.append(
        convert_value(country_data2[col])
    )


# ---------------- BAR CHART ----------------

comparison_df = pd.DataFrame({

    "Indicator": cols,

    country1: values1,

    country2: values2

})

st.dataframe(comparison_df)


fig, ax = plt.subplots(figsize=(10, 5))

x = range(len(cols))

width = 0.35

ax.bar(
    [i - width / 2 for i in x],
    values1,
    width,
    label=country1
)

ax.bar(
    [i + width / 2 for i in x],
    values2,
    width,
    label=country2
)

ax.set_xticks(x)

ax.set_xticklabels(
    cols,
    rotation=45,
    ha="right"
)

ax.set_ylabel("Value")

ax.set_title(
    f"{country1} vs {country2}"
)

ax.legend()

st.pyplot(fig)


# ---------------- HIGHEST VALUE COMPARISON ----------------

st.subheader("🏆 Highest Value Comparison")

results = []

for i in range(len(cols)):

    indicator = cols[i]

    value1 = values1[i]

    value2 = values2[i]

    if value1 > value2:

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
    use_container_width=True
)


# ---------------- FINAL RESULT ----------------

st.subheader("🏅 Final Comparison Result")

country1_wins = 0

country2_wins = 0

for i in range(len(cols)):

    if values1[i] > values2[i]:

        country1_wins += 1

    elif values2[i] > values1[i]:

        country2_wins += 1


col1, col2 = st.columns(2)

with col1:

    st.metric(
        f"{country1} Wins",
        country1_wins
    )

with col2:

    st.metric(
        f"{country2} Wins",
        country2_wins
    )


if country1_wins > country2_wins:

    st.success(
        f"🏆 {country1} has the highest values in more indicators!"
    )

elif country2_wins > country1_wins:

    st.success(
        f"🏆 {country2} has the highest values in more indicators!"
    )

else:

    st.info(
        "🤝 Both countries have an equal number of wins!"
    )


# ---------------- COUNTRY DETAILS ----------------

st.subheader(f"📋 {country1} Details")

st.dataframe(
    df[df["Country"] == country1],
    use_container_width=True
)


st.subheader(f"📋 {country2} Details")

st.dataframe(
    df[df["Country"] == country2],
    use_container_width=True
)
