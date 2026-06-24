import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="RetailPulse - Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 RetailPulse - Sales Dashboard")
st.markdown("Analyze revenue, orders, products, customers and sales trends.")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "../data/cleaned_retail.csv",
        parse_dates=["InvoiceDate"]
    )
    return df

df = load_data()

# =====================================================
# FEATURE ENGINEERING
# =====================================================

df["Date"] = df["InvoiceDate"].dt.date
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month_name()
df["Weekday"] = df["InvoiceDate"].dt.day_name()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("📌 Filters")

# Date Filter

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Country Filter

country_options = sorted(
    df["Country"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "Select Country",
    country_options,
    default=country_options
)

# Product Filter

product_options = sorted(
    df["Description"].dropna().unique()
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    product_options
    
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"] >= start_date)
        &
        (filtered_df["InvoiceDate"] <= end_date)
    ]

filtered_df = filtered_df[
    filtered_df["Country"].isin(selected_countries)
]

if selected_products:

    filtered_df = filtered_df[
        filtered_df["Description"].isin(
            selected_products
        )
    ]

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = filtered_df["Sales"].sum()

total_orders = (
    filtered_df["InvoiceNo"]
    .nunique()
)

total_customers = (
    filtered_df["CustomerID"]
    .nunique()
)

avg_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.0f}"
    )

with kpi2:
    st.metric(
        "🧾 Orders",
        f"{total_orders:,}"
    )

with kpi3:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with kpi4:
    st.metric(
        "📦 Avg Order Value",
        f"₹{avg_order_value:,.2f}"
    )

# =====================================================
# VISUAL 1
# MONTHLY SALES TREND
# =====================================================

monthly_sales = (
    filtered_df.groupby(
        pd.Grouper(
            key="InvoiceDate",
            freq="M"
        )
    )["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# VISUALS 2 & 3
# =====================================================

col1, col2 = st.columns(2)

with col1:

    daily_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Daily Sales Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    monthly_orders = (
        filtered_df.groupby('Month')['InvoiceNo']
              
        .nunique()
        .reset_index()
    )

    fig3 = px.bar(
        monthly_orders,
        x="Month",
        y="InvoiceNo",
        title="Monthly Orders"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================================
# VISUALS 4 & 5
# =====================================================

col1, col2 = st.columns(2)

with col1:

    top_revenue_products = (
        filtered_df.groupby(
            "Description"
        )["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top_revenue_products,
        x="Sales",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with col2:

    top_quantity_products = (
        filtered_df.groupby(
            "Description"
        )["Quantity"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        top_quantity_products,
        x="Quantity",
        y="Description",
        orientation="h",
        title="Top 10 Products by Quantity"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# =====================================================
# VISUALS 6 & 7
# =====================================================

col1, col2 = st.columns(2)

country_sales = (
    filtered_df.groupby("Country")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

with col1:

    fig6 = px.pie(
        country_sales,
        values="Sales",
        names="Country",
        title="Revenue by Country"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

with col2:

    fig7 = px.bar(
        country_sales,
        x="Country",
        y="Sales",
        title="Top Countries by Revenue"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# =====================================================
# VISUAL 8
# =====================================================

fig8 = px.histogram(
    filtered_df,
    x="Sales",
    nbins=50,
    title="Sales Distribution"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# =====================================================
# VISUALS 9 & 10
# =====================================================

col1, col2 = st.columns(2)

with col1:

    revenue_month = (
        filtered_df.groupby(
            "Month"
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig9 = px.bar(
        revenue_month,
        x="Month",
        y="Sales",
        title="Revenue by Month"
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )

with col2:

    orders_month = (
        filtered_df.groupby(
            "Month"
        )["InvoiceNo"]
        .nunique()
        .reset_index()
    )

    fig10 = px.bar(
        orders_month,
        x="Month",
        y="InvoiceNo",
        title="Orders by Month"
    )

    st.plotly_chart(
        fig10,
        use_container_width=True
    )

# =====================================================
# VISUALS 11 & 12
# =====================================================

col1, col2 = st.columns(2)

with col1:

    weekday_sales = (
        filtered_df.groupby(
            "Weekday"
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig11 = px.bar(
        weekday_sales,
        x="Weekday",
        y="Sales",
        title="Revenue by Weekday"
    )

    st.plotly_chart(
        fig11,
        use_container_width=True
    )

with col2:

    top_customers = (
        filtered_df.groupby(
            "CustomerID"
        )["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    fig12 = px.bar(
        top_customers,
        x="CustomerID",
        y="Sales",
        title="Top 10 Customers"
    )

    st.plotly_chart(
        fig12,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.subheader("📥 Export Data")

st.download_button(
    label="Download Filtered Dataset",
    data=filtered_df.to_csv(
        index=False
    ),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER 
# =====================================================

st.markdown("---")
st.markdown(
    "RetailPulse | Sales Analytics Dashboard"
)

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("➡ Go To Customer Dashboard"):
        st.switch_page("pages/Customer_Dashboard.py")