import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Optimization Dashboard")

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "../data/inventory_optimization.csv"
    )

inventory = load_data()

# ==========================================
# FILTERS
# ==========================================

st.sidebar.header("Inventory Filters")

selected_metrics = st.sidebar.multiselect(
    "Select Metrics",
    inventory["Metric"].unique(),
    default=inventory["Metric"].unique()
)

filtered = inventory[
    inventory["Metric"].isin(
        selected_metrics
    )
]

# ==========================================
# KPI CARDS
# ==========================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Metrics",
    len(filtered)
)

c2.metric(
    "Max Value",
    f"{filtered['Value'].max():,.0f}"
)

c3.metric(
    "Min Value",
    f"{filtered['Value'].min():,.0f}"
)

c4.metric(
    "Average",
    f"{filtered['Value'].mean():,.0f}"
)

st.divider()

# ==========================================
# VISUAL 1
# ==========================================

fig1 = px.bar(
    filtered,
    x="Metric",
    y="Value",
    color="Metric",
    title="Inventory Metrics"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# VISUAL 2
# ==========================================

fig2 = px.pie(
    filtered,
    names="Metric",
    values="Value",
    title="Metric Contribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# VISUAL 3
# ==========================================

fig3 = px.treemap(
    filtered,
    path=["Metric"],
    values="Value",
    title="Inventory Treemap"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# VISUAL 4
# ==========================================

fig4 = px.funnel(
    filtered,
    x="Value",
    y="Metric",
    title="Inventory Funnel"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# VISUAL 5
# ==========================================

fig5 = px.scatter(
    filtered,
    x="Metric",
    y="Value",
    size="Value",
    color="Metric",
    title="Metric Comparison"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==========================================
# VISUAL 6
# ==========================================

fig6 = px.area(
    filtered,
    x="Metric",
    y="Value",
    title="Inventory Area Analysis"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ==========================================
# VISUAL 7
# ==========================================

fig7 = px.line(
    filtered,
    x="Metric",
    y="Value",
    markers=True,
    title="Inventory Trend"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# ==========================================
# VISUAL 8
# ==========================================

st.subheader("Inventory Optimization Table")

st.dataframe(
    filtered,
    use_container_width=True
)

# ==========================================
# RECOMMENDATION BOX
# ==========================================

st.subheader("📌 Inventory Recommendations")

for _, row in filtered.iterrows():
    st.info(
        f"{row['Metric']} : {row['Value']:,.0f}"
    )

# ==========================================
# NAVIGATION
# ==========================================

st.divider()

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("⬅ Forecast Dashboard"):
        st.switch_page(
            "pages/3_📊_Forecast_Dashboard.py"
        )

with col3:
    if st.button("🏠 Sales Dashboard"):
        st.switch_page(
            "pages/Sales_Dashboard.py"
        )