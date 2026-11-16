"""Activity 1 starter: a deliberately notebook-style Streamlit app.

Goal (30 min): run it, finish the TODOs, push it to GitHub and deploy it
on Streamlit Community Cloud. Everything is in ONE file on purpose:
Activity 2 refactors it into modules.

Run from the kit root:   streamlit run session1/activity1_starter/app.py

When you move this app to YOUR OWN repo: copy data/sales_daily.csv next to
app.py and change DATA to Path(__file__).parent / "sales_daily.csv".
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent / "sales_daily.csv"

st.set_page_config(page_title="Sales Explorer", layout="wide")
st.title("Sales Explorer")

df = pd.read_csv(DATA, parse_dates=["date"])

# TODO 1: region filter
regions = sorted(df["region"].unique())
sel_regions = st.sidebar.multiselect("Region", regions, default=regions)

# TODO 2: category filter
categories = sorted(df["category"].unique())
sel_categories = st.sidebar.multiselect("Category", categories, default=categories)

df = df[df["region"].isin(sel_regions) & df["category"].isin(sel_categories)]

if df.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# TODO 3: KPI cards
c1, c2, c3 = st.columns(3)
c1.metric("Total units", f"{df['units'].sum():,.0f}")
c2.metric("Revenue", f"${df['revenue'].sum():,.0f}")
c3.metric("# SKUs", df["sku"].nunique())

daily = df.groupby("date", as_index=False)["units"].sum()
fig = px.line(daily, x="date", y="units", title="Daily units")
st.plotly_chart(fig, width="stretch")

# TODO 4: top 10 SKUs by revenue
top10 = (df.groupby("sku", as_index=False)["revenue"].sum()
           .nlargest(10, "revenue")
           .sort_values("revenue"))
fig2 = px.bar(top10, x="revenue", y="sku", orientation="h", title="Top 10 SKUs by revenue")
st.plotly_chart(fig2, width="stretch")

# TODO 5 (stretch): filtered rows
with st.expander("Show filtered rows"):
    st.dataframe(df, width="stretch", hide_index=True)
