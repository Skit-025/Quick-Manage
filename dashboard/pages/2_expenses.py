import os
import sys
import streamlit as st
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from analytics.reports import get_expenses_dataframe
from database.db_manager import DatabaseManager
from database.models import Expense


def show():
	st.title("Expenses")
	st.caption("View and add expenses")

	try:
		db = DatabaseManager()
		df = get_expenses_dataframe(db, user_id=1)
	except Exception as exc:
		st.error(f"Unable to load data: {exc}")
		return

	st.subheader("Recent expenses")
	if df.empty:
		st.info("No expenses recorded.")
	else:
		st.dataframe(df)

	st.subheader("Add expense")
	with st.form("add_expense"):
		category = st.number_input("Category ID", min_value=1, value=1)
		amount = st.number_input("Amount", min_value=0.0, value=100.0, format="%.2f")
		desc = st.text_input("Description")
		date_str = st.text_input("Date (YYYY-MM-DD)", value=str(date.today()))
		submitted = st.form_submit_button("Add")

	if submitted:
		try:
			dt = date.fromisoformat(date_str)
			exp = Expense(user_id=1, category_id=int(category), amount=float(amount), date_=dt, description_=desc)
			eid = db.add_expense(exp)
			st.success(f"Expense added: id {eid}")
			st.experimental_rerun()
		except Exception as e:
			st.error(f"Failed to add expense: {e}")

if __name__ == "__main__":
    show()