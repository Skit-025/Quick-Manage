import os
import sys
import streamlit as st
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from analytics.reports import get_expenses_dataframe, monthly_summary
from database.db_manager import DatabaseManager


def show():
	st.title("Charts")
	st.caption("Visualize spending trends")

	try:
		db = DatabaseManager()
		df = get_expenses_dataframe(db, user_id=1)
	except Exception as exc:
		st.error(f"Unable to load data: {exc}")
		return

	if df.empty:
		st.info("No expense data available.")
		return

	summary = monthly_summary(df).reset_index()
	if summary.empty:
		st.info("Not enough data to show charts.")
		return

	summary['total_amount'] = summary['total_amount'].astype(float)
	st.subheader("Monthly spending")
	st.bar_chart(data=summary.set_index('month')['total_amount'])

if __name__ == "__main__":
    show()