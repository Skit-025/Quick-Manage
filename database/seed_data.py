import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from database.models import User, Category, Expense, Budget
from database.exception import DuplicateEntryError
from datetime import date

db = DatabaseManager()

# ── USERS ─────────────────────────────────────────────────────
try:
    user_id = db.add_user(User(name="Rahul", email="rahul@gmail.com", password="pass123"))
    print(f"User added with id: {user_id}")
except DuplicateEntryError:
    print("User already exists, skipping")
    user_id = 1

# ── CATEGORIES ────────────────────────────────────────────────
categories = [
    Category(name="Food", budget_limit=5000),
    Category(name="Transport", budget_limit=2000),
    Category(name="Entertainment", budget_limit=1500),
    Category(name="Shopping", budget_limit=3000),
    Category(name="Health", budget_limit=2000),
    Category(name="Utilities", budget_limit=1000),
]

cat_ids = {}
for cat in categories:
    try:
        cid = db.add_category(cat)
        cat_ids[cat.name] = cid
        print(f"Category added: {cat.name}")
    except DuplicateEntryError:
        print(f"Category exists, skipping: {cat.name}")
        all_cats = db.get_all_categories()
        cat_ids = {c.name: c.id for c in all_cats}

# ── EXPENSES ──────────────────────────────────────────────────
expenses = [
    Expense(user_id=user_id, category_id=cat_ids["Food"], amount=180, date_=date(2026, 6, 1), description_="Lunch"),
    Expense(user_id=user_id, category_id=cat_ids["Transport"], amount=60, date_=date(2026, 6, 2), description_="Auto"),
    Expense(user_id=user_id, category_id=cat_ids["Food"], amount=350, date_=date(2026, 6, 3), description_="Dinner"),
    Expense(user_id=user_id, category_id=cat_ids["Shopping"], amount=1200, date_=date(2026, 6, 4), description_="Clothes"),
    Expense(user_id=user_id, category_id=cat_ids["Health"], amount=500, date_=date(2026, 6, 5), description_="Medicine"),
    Expense(user_id=user_id, category_id=cat_ids["Entertainment"], amount=299, date_=date(2026, 6, 6), description_="Netflix"),
    Expense(user_id=user_id, category_id=cat_ids["Utilities"], amount=800, date_=date(2026, 6, 7), description_="Electricity"),
    Expense(user_id=user_id, category_id=cat_ids["Food"], amount=220, date_=date(2026, 6, 8), description_="Groceries"),
    Expense(user_id=user_id, category_id=cat_ids["Transport"], amount=150, date_=date(2026, 6, 9), description_="Uber"),
    Expense(user_id=user_id, category_id=cat_ids["Food"], amount=400, date_=date(2026, 6, 10), description_="Restaurant"),
]

for exp in expenses:
    eid = db.add_expense(exp)
    print(f"Expense added: ₹{exp.amount} — {exp.description_}")

# ── BUDGETS ───────────────────────────────────────────────────
budgets = [
    Budget(user_id=user_id, category_id=cat_ids["Food"], amount=5000, month_="2026-06"),
    Budget(user_id=user_id, category_id=cat_ids["Transport"], amount=2000, month_="2026-06"),
    Budget(user_id=user_id, category_id=cat_ids["Entertainment"], amount=1500, month_="2026-06"),
    Budget(user_id=user_id, category_id=cat_ids["Shopping"], amount=3000, month_="2026-06"),
]

for bud in budgets:
    bid = db.add_budget(bud)
    print(f"Budget added: ₹{bud.amount} for {bud.month_}")

print("\nSeed data loaded successfully!")