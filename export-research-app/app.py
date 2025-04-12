# app.py
import streamlit as st
import datetime
import pandas as pd
from comtrade_api import fetch_comtrade_data

# 🧾 Page config
st.set_page_config(page_title="Export Research Tool", layout="wide")

# 🎯 Sidebar Inputs
st.sidebar.title("🔍 Product & Market Research")
product_name = st.sidebar.text_input("Enter Product Name (e.g. Coffee, Rice, Cotton)", "Coffee")
market_name = st.sidebar.text_input("Enter Country Name (e.g. United States, Germany)", "United States")
year_range = st.sidebar.selectbox("Select Year Range", ["Last 1 year", "Last 3 years", "Last 5 years", "Last 10 years"])
submit = st.sidebar.button("Get Export Insights")

# 🌍 Convert readable years
current_year = datetime.datetime.now().year
year_mapping = {
    "Last 1 year": [current_year],
    "Last 3 years": list(range(current_year - 2, current_year + 1)),
    "Last 5 years": list(range(current_year - 4, current_year + 1)),
    "Last 10 years": list(range(current_year - 9, current_year + 1)),
}
selected_years = year_mapping[year_range]

# 🧠 Hardcoded mappings (for now, can be dynamic later)
product_hs_code = "0901"  # Coffee HS Code
reporter_code = "356"     # India
partner_code = "842"      # United States

# 🧩 Your API Key (from you)
api_key = "1fWn8kDPrMtwvR92ftNfNMhcgFYhJk7IKqxrtX9a"

# ▶️ Logic runs after Submit
if submit:
    st.title(f"📈 Export Trends for {product_name} to {market_name}")
    results = []

    for year in selected_years:
        params = {
            "typeCode": "C",
            "freqCode": "A",
            "clCode": "HS",
            "reporterCode": reporter_code,
            "cmdCode": product_hs_code,
            "period": year,
            "flowCode": "X",  # Export
            "partnerCode": partner_code
        }
        data = fetch_comtrade_data(params, api_key)
        if data and data.get("data"):
            results.extend(data["data"])

    if results:
        df = pd.DataFrame(results)
        st.subheader("🧾 Raw Export Data from UN Comtrade")
        st.dataframe(df[["period", "reporterDesc", "partnerDesc", "cmdDescE", "netWeight", "primaryValue"]])
    else:
        st.warning("No data found. Please check product or market name.")
