import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Forecast Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Demand Forecast Dashboard")
st.markdown(
    "Prophet • LSTM • Hybrid Forecasting • What-If Analysis"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    forecast = pd.read_csv(
        "data/forcast_result.csv"
    )

    forecast["ds"] = pd.to_datetime(
        forecast["ds"]
    )

    return forecast

forecast = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Forecast Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    (
        forecast["ds"].min(),
        forecast["ds"].max()
    )
)

growth_factor = st.sidebar.slider(
    "Demand Adjustment %",
    -50,
    100,
    0
)

# =====================================================
# FILTER DATA
# =====================================================

filtered = forecast.copy()

if len(date_range) == 2:

    filtered = filtered[
        (
            filtered["ds"] >= pd.to_datetime(date_range[0])
        )
        &
        (
            filtered["ds"] <= pd.to_datetime(date_range[1])
        )
    ]

# =====================================================
# WHAT IF ANALYSIS
# =====================================================

filtered["Adjusted_Forecast"] = (
    filtered["yhat"]
    * (1 + growth_factor / 100)
)

# =====================================================
# KPI CARDS
# =====================================================

latest_forecast = filtered["yhat"].iloc[-1]

avg_forecast = filtered["yhat"].mean()

max_forecast = filtered["yhat"].max()

min_forecast = filtered["yhat"].min()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Latest Forecast",
    f"{latest_forecast:.0f}"
)

c2.metric(
    "Average Demand",
    f"{avg_forecast:.0f}"
)

c3.metric(
    "Maximum Forecast",
    f"{max_forecast:.0f}"
)

c4.metric(
    "Minimum Forecast",
    f"{min_forecast:.0f}"
)

st.divider()

# =====================================================
# VISUAL 1
# FORECAST TREND
# =====================================================

fig1 = px.line(
    filtered,
    x="ds",
    y="yhat",
    title="Demand Forecast Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# VISUAL 2
# WHAT IF ANALYSIS
# =====================================================

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=filtered["ds"],
        y=filtered["yhat"],
        name="Original Forecast"
    )
)

fig2.add_trace(
    go.Scatter(
        x=filtered["ds"],
        y=filtered["Adjusted_Forecast"],
        name="Adjusted Forecast"
    )
)

fig2.update_layout(
    title="What-If Demand Analysis"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# VISUAL 3 + 4
# =====================================================

col1,col2 = st.columns(2)

with col1:

    fig3 = px.histogram(
        filtered,
        x="yhat",
        nbins=30,
        title="Forecast Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:

    filtered["Month"] = (
        filtered["ds"]
        .dt.month_name()
    )

    monthly = (
        filtered.groupby("Month")
        ["yhat"]
        .mean()
        .reset_index()
    )

    fig4 = px.bar(
        monthly,
        x="Month",
        y="yhat",
        title="Average Monthly Forecast"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================================
# VISUAL 5
# WEEKLY FORECAST
# =====================================================

filtered["Week"] = (
    filtered["ds"]
    .dt.isocalendar()
    .week
)

weekly = (
    filtered.groupby("Week")
    ["yhat"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    weekly,
    x="Week",
    y="yhat",
    title="Weekly Forecast"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =====================================================
# VISUAL 6
# FORECAST COMPONENTS IMAGE
# =====================================================

st.subheader(
    "Forecast Components"
)

try:
    st.image(
        "pngs/forecast_components.png",
        use_container_width=True
    )
except:
    st.warning(
        "forecast_components.png not found"
    )

# =====================================================
# VISUAL 7
# DEMAND FORECAST IMAGE
# =====================================================

st.subheader(
    "Prophet Forecast Output"
)

try:
    st.image(
        "pngs/demand_forcast.png",
        use_container_width=True
    )
except:
    st.warning(
        "demand_forcast.png not found"
    )

# =====================================================
# VISUAL 8
# FORECAST TABLE
# =====================================================

st.subheader(
    "Forecast Data"
)

st.dataframe(
    filtered.tail(20),
    use_container_width=True
)

# =====================================================
# NAVIGATION
# =====================================================

st.divider()

col1,col2,col3 = st.columns(3)

with col1:
    if st.button(
        "⬅ Customer Dashboard"
    ):
        st.switch_page(
            "pages/2_👥_Customer_Dashboard.py"
        )

with col3:
    if st.button(
        "Inventory Dashboard ➡"
    ):
        st.switch_page(
            "pages/Inventory_Dashboard.py"
        )