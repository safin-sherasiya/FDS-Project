from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail Demand Predictor", page_icon="📦")
st.title("Retail Demand Predictor")
st.write("Select a product category and date to estimate demand.")

forecast_path = Path("outputs/future_demand_forecast.csv")
if not forecast_path.exists():
    st.error("Forecast file not found. Run all cells in Retail_Demand_Forecasting.ipynb first.")
    st.stop()

forecast = pd.read_csv(forecast_path, parse_dates=["Date"])
if forecast.empty:
    st.error("Forecast file is empty. Run the notebook again.")
    st.stop()

categories = sorted(forecast["Category"].dropna().astype(str).unique())
min_date = forecast["Date"].min().date()
max_date = forecast["Date"].max().date()

category = st.selectbox("Category", categories)
selected_date = st.date_input(
    "Forecast date", value=min_date, min_value=min_date, max_value=max_date
)

if st.button("Predict demand", type="primary"):
    result = forecast[
        (forecast["Category"].astype(str) == category) &
        (forecast["Date"].dt.date == selected_date)
    ]
    if result.empty:
        st.warning("No prediction found for this selection.")
    else:
        predicted = float(result.iloc[0]["Forecast_Demand"])
        st.metric("Predicted demand (units)", f"{predicted:,.0f}")
        st.write(f"Category: **{category}**")
        st.write(f"Date: **{selected_date:%d %b %Y}**")
        st.caption("This is an estimate, not a guaranteed sales quantity.")

st.caption(f"Available forecast dates: {min_date:%d %b %Y} – {max_date:%d %b %Y}")
