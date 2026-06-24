import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Customer Dashboard",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analytics Dashboard")
st.markdown("Customer Segmentation • Churn Analysis • RFM Insights")

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    segments = pd.read_csv("../data/customer_segments.csv")

    churn = pd.read_csv(
        "../data/customer_churn_predictions.csv"
    )

    return segments, churn


segments, churn = load_data()


st.sidebar.header("🔍 Customer Filters")

cluster_filter = st.sidebar.multiselect(
    "Customer Segment",
    sorted(segments["Cluster"].unique()),
    default=sorted(segments["Cluster"].unique())
)

recency_filter = st.sidebar.slider(
    "Recency",
    int(segments["Recency"].min()),
    int(segments["Recency"].max()),
    (
        int(segments["Recency"].min()),
        int(segments["Recency"].max())
    )
)

frequency_filter = st.sidebar.slider(
    "Frequency",
    int(segments["Frequency"].min()),
    int(segments["Frequency"].max()),
    (
        int(segments["Frequency"].min()),
        int(segments["Frequency"].max())
    )
)

monetary_filter = st.sidebar.slider(
    "Monetary",
    int(segments["Monetary"].min()),
    int(segments["Monetary"].max()),
    (
        int(segments["Monetary"].min()),
        int(segments["Monetary"].max())
    )
)

# ======================================================
# FILTER DATA
# ======================================================

filtered_segments = segments[
    (segments["Cluster"].isin(cluster_filter))
    &
    (segments["Recency"] >= recency_filter[0])
    &
    (segments["Recency"] <= recency_filter[1])
    &
    (segments["Frequency"] >= frequency_filter[0])
    &
    (segments["Frequency"] <= frequency_filter[1])
    &
    (segments["Monetary"] >= monetary_filter[0])
    &
    (segments["Monetary"] <= monetary_filter[1])
]

# ======================================================
# KPI SECTION
# ======================================================

total_customers = len(filtered_segments)

cluster_count = filtered_segments["Cluster"].nunique()

avg_frequency = filtered_segments[
    "Frequency"
].mean()

avg_monetary = filtered_segments[
    "Monetary"
].mean()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Segments",
    cluster_count
)

c3.metric(
    "Avg Frequency",
    f"{avg_frequency:.1f}"
)

c4.metric(
    "Avg Monetary",
    f"${avg_monetary:.2f}"
)

st.divider()

# ======================================================
# VISUAL 1
# SEGMENT DISTRIBUTION
# ======================================================

segment_counts = (
    filtered_segments["Cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

segment_counts.columns = [
    "Cluster",
    "Customers"
]

fig1 = px.bar(
    segment_counts,
    x="Cluster",
    y="Customers",
    title="Customer Segment Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# VISUAL 2 + 3
# ======================================================

col1,col2 = st.columns(2)

with col1:

    fig2 = px.pie(
        segment_counts,
        names="Cluster",
        values="Customers",
        title="Segment Share"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    fig3 = px.histogram(
        filtered_segments,
        x="Recency",
        nbins=30,
        title="Recency Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ======================================================
# VISUAL 4 + 5
# ======================================================

col1,col2 = st.columns(2)

with col1:

    fig4 = px.histogram(
        filtered_segments,
        x="Frequency",
        nbins=30,
        title="Frequency Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with col2:

    fig5 = px.histogram(
        filtered_segments,
        x="Monetary",
        nbins=30,
        title="Monetary Distribution"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ======================================================
# VISUAL 6
# CUSTOMER VALUE SCATTER
# ======================================================

fig6 = px.scatter(
    filtered_segments,
    x="Frequency",
    y="Monetary",
    color="Cluster",
    size="Monetary",
    hover_data=["CustomerID"],
    title="Customer Value Analysis"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ======================================================
# VISUAL 7
# RECENCY VS FREQUENCY
# ======================================================

fig7 = px.scatter(
    filtered_segments,
    x="Recency",
    y="Frequency",
    color="Cluster",
    title="Recency vs Frequency"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# ======================================================
# VISUAL 8
# MONETARY BY SEGMENT
# ======================================================

fig8 = px.box(
    filtered_segments,
    x="Cluster",
    y="Monetary",
    color="Cluster",
    title="Monetary Distribution by Segment"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# ======================================================
# TOP CUSTOMERS
# ======================================================

st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_segments
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers,
    use_container_width=True
)

# ======================================================
# NAVIGATION
# ======================================================

st.divider()

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("⬅ Sales Dashboard"):
        st.switch_page(
            "pages/1_📈_Sales_Dashboard.py"
        )

with col3:
    if st.button("Forecast Dashboard ➡"):
        st.switch_page(
            "pages/Forecast_Dashboard.py"
        )