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
		category = st.number_input("Category ID", min_value=1, value=1, key='add_expense_category')
		amount = st.number_input("Amount", min_value=0.0, value=100.0, format="%.2f", key='add_expense_amount')
		desc = st.text_input("Description", key='add_expense_desc')
		date_str = st.text_input("Date (YYYY-MM-DD)", value=str(date.today()), key='add_expense_date')
		submitted = st.form_submit_button("Add")

	if submitted:
		try:
			dt = date.fromisoformat(date_str)
			exp = Expense(user_id=1, category_id=int(category), amount=float(amount), date_=dt, description_=desc)
			eid = db.add_expense(exp)
			st.success(f"Expense added: id {eid}")
			# Refresh the displayed expenses without relying on experimental API
			try:
				# Clear form fields via session state
				st.session_state['add_expense_category'] = 1
				st.session_state['add_expense_amount'] = 0.0
				st.session_state['add_expense_desc'] = ''
				st.session_state['add_expense_date'] = str(date.today())
			except Exception:
				pass
			# Re-fetch and display updated expenses
			try:
				df = get_expenses_dataframe(db, user_id=1)
				if not df.empty:
					st.dataframe(df)
			except Exception:
				pass
		except Exception as e:
			st.error(f"Failed to add expense: {e}")

if __name__ == "__main__":
    show()