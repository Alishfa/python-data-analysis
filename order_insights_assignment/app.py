#10. Build Your Dashboard
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide" )
st.title("Sales Dashboard")

df = pd.read_csv("output/cleaned_orders.csv", parse_dates=["order_date"])

st.sidebar.header("Filters orders")

regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())

selected_region = st.sidebar.selectbox("Select Region", ["All"] + regions)
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
c1,c2,c3 = st.columns(3)
c1.metric("Total Orders", f"{len(filtered_df):,}")
c2.metric("Total Sales", f"${filtered_df['order_value'].sum():,.2f}")
c3.metric("Average Order Value", f"${filtered_df['order_value'].mean():,.2f}" if len(filtered_df) > 0 else "$0.00")
st.divider()

#sales chart
st.subheader("Sales by Category & Region")
if not filtered_df.empty:
    sales_by_category = filtered_df.groupby("category")["order_value"].sum().reset_index()
    st.bar_chart(sales_by_category.set_index("category"))
else:
    st.warning("No data available for the selected filters.")

# 7. Filtered Data Table
st.subheader("Filtered Orders Data")
st.dataframe(filtered_df, use_container_width=True)

