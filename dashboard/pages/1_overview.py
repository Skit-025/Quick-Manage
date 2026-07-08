import streamlit as st
import pandas as pd

from analytics.reports import get_expenses_dataframe, monthly_summary, top_spending_category
from database.db_manager import DatabaseManager


def show():
	st.title("Overview")
	st.caption("Summary of your recent spending")

	try:
		db = DatabaseManager()
		df = get_expenses_dataframe(db, user_id=1)
	except Exception as exc:
		st.error(f"Unable to load data: {exc}")
		return

	if df.empty:
		st.info("No expense data available. Run `python database/seed_data.py` to add sample data.")
		return

	summary = monthly_summary(df)
	st.subheader("Monthly Totals")
	st.dataframe(summary)

	cat_id, amount = top_spending_category(df)
	if cat_id is not None:
		st.metric("Top category id", f"{cat_id}", delta=f"₹{amount:,.2f}")
