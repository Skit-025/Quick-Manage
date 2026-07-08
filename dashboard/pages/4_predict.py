import os
import sys
import streamlit as st
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from analytics.reports import get_expenses_dataframe
from database.db_manager import DatabaseManager
from ml.predictor import forecast_monthly_spend, predict_next_month_spend


def show():
    st.title("Expense Prediction")
    st.caption("Estimate upcoming monthly spending from your historical expenses.")

    try:
        db = DatabaseManager()
        user_id = 1
        df = get_expenses_dataframe(db, user_id=user_id)
    except Exception as exc:
        st.error(f"Unable to load expense data: {exc}")
        return

    if df.empty:
        st.info("No expense data is available yet. Add a few expenses to see forecasts.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        months_ahead = st.slider("Forecast horizon (months)", min_value=1, max_value=6, value=3)

    with col2:
        st.metric("Next month estimate", f"₹{predict_next_month_spend(df, months_ahead=1):,.2f}")

    forecast = forecast_monthly_spend(df, months_ahead=months_ahead)

    if forecast:
        st.subheader("Forecasted monthly spending")
        forecast_df = pd.DataFrame(
            {
                "Month": [f"Month {i}" for i in range(1, len(forecast) + 1)],
                "Estimated Spend": forecast,
            }
        )
        st.bar_chart(forecast_df.set_index("Month"))

        st.dataframe(forecast_df, use_container_width=True)
    else:
        st.warning("Not enough data to generate a forecast.")


if __name__ == "__main__":
    show()
