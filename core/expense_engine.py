"""
core/expense_engine.py — Module 2: Core Engine
------------------------------------------------
Generators and iterators for streaming expenses without loading everything
into memory at once.

DatabaseManager.get_expenses() (Module 1) uses fetchall(), which pulls every
row into a Python list before you touch a single one. Fine for small data,
wasteful for years of daily expenses. The functions below iterate the sqlite3
cursor directly — rows are only pulled from disk as you ask for the next one.
"""

import os
import sys
import logging
from itertools import islice, groupby

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import APP_NAME
from models import Expense
from core.exceptions import StreamError

logger = logging.getLogger(APP_NAME)


# ── Core stream ──────────────────────────────────────────────────────────────

def stream_expenses(db, user_id: int):
    """
    Yield Expense objects for a user, one row at a time, straight from the
    sqlite3 cursor. Never materializes the full result set.
    """
    conn = db._getConnection()
    try:
        cursor = conn.execute(
            "SELECT * FROM EXPENSES WHERE USER_ID = ? ORDER BY DATE_ DESC",
            (user_id,)
        )
        for row in cursor:
            yield Expense(
                id=row["ID"], user_id=row["USER_ID"], category_id=row["CATEGORY_ID"],
                amount=row["AMOUNT"], description_=row["DESCRIPTION_"], date_=row["DATE_"]
            )
    except Exception as e:
        raise StreamError(f"stream_expenses failed: {e}")
    finally:
        conn.close()


# ── Pipeline helpers (each takes/returns an iterator — compose freely) ──────

def filter_by_category(expense_stream, category_id: int):
    """Yield only the expenses in expense_stream matching category_id."""
    for expense in expense_stream:
        if expense.category_id == category_id:
            yield expense


def filter_by_amount(expense_stream, min_amount: float = 0.0, max_amount: float = float("inf")):
    """Yield only expenses whose amount falls within [min_amount, max_amount]."""
    for expense in expense_stream:
        if min_amount <= expense.amount <= max_amount:
            yield expense


def running_total(expense_stream):
    """Yield (expense, total_so_far) tuples without ever storing the full list."""
    total = 0.0
    for expense in expense_stream:
        total += expense.amount
        yield expense, round(total, 2)


def batch(expense_stream, batch_size: int = 50):
    """
    Chunk a stream into lists of batch_size. Useful for background report
    generation (Module 4) where you want to hand off work in manageable pieces
    instead of one record at a time or the whole dataset at once.
    """
    if batch_size <= 0:
        raise StreamError("batch_size must be a positive integer")
    stream = iter(expense_stream)
    while True:
        chunk = list(islice(stream, batch_size))
        if not chunk:
            return
        yield chunk


def group_by_month(expense_stream):
    """
    Yield (month, [expenses]) pairs. Assumes rows arrive ordered by DATE_
    (true for stream_expenses, which orders DESC) — groupby only groups
    consecutive matching keys, so unsorted input will produce duplicate groups.
    """
    def month_key(expense):
        return str(expense.date_)[:7]  # 'YYYY-MM'

    for month, group in groupby(expense_stream, key=month_key):
        yield month, list(group)


def take(expense_stream, n: int):
    """Yield only the first n items — handy for previews without full loads."""
    return islice(expense_stream, n)