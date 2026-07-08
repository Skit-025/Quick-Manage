"""
core/file_handler.py — Module 2: Core Engine
-----------------------------------------------
CSV import/export for expenses.

Export streams from the database straight to disk (via expense_engine.stream_expenses)
so a large history never sits fully in memory. Import reads the CSV lazily with
csv.DictReader (which is itself a generator over file lines) and validates each
row before it ever reaches the database.
"""

import os
import sys
import csv
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import APP_NAME
from models import Expense
from core.exceptions import FileImportError, FileExportError, ValidationError
from core.expense_engine import stream_expenses
from core.decorators import log_activity

logger = logging.getLogger(APP_NAME)

CSV_FIELDS = ["id", "user_id", "category_id", "amount", "description_", "date_"]


# ── Export ───────────────────────────────────────────────────────────────────

@log_activity
def export_expenses_to_csv(db, user_id: int, filepath: str) -> int:
    """
    Stream a user's expenses straight to a CSV file. Returns the row count.
    Raises FileExportError on any I/O problem.
    """
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        row_count = 0
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for expense in stream_expenses(db, user_id):
                writer.writerow({
                    "id": expense.id,
                    "user_id": expense.user_id,
                    "category_id": expense.category_id,
                    "amount": expense.amount,
                    "description_": expense.description_ or "",
                    "date_": expense.date_,
                })
                row_count += 1
        logger.info(f"Exported {row_count} expenses to {filepath}")
        return row_count
    except OSError as e:
        raise FileExportError(f"Could not write to {filepath}: {e}")
    except Exception as e:
        raise FileExportError(f"export_expenses_to_csv failed: {e}")


# ── Import ───────────────────────────────────────────────────────────────────

def _parse_row(row: dict, line_number: int) -> Expense:
    """Turn one CSV row into an Expense, or raise ValidationError with context."""
    try:
        amount = float(row["amount"])
        if amount <= 0:
            raise ValidationError(f"Line {line_number}: amount must be greater than 0")

        date_str = row["date_"].strip()
        date_val = datetime.strptime(date_str, "%Y-%m-%d").date()

        return Expense(
            user_id=int(row["user_id"]),
            category_id=int(row["category_id"]),
            amount=amount,
            description_=row.get("description_") or None,
            date_=date_val,
        )
    except (KeyError, ValueError) as e:
        raise ValidationError(f"Line {line_number}: malformed row — {e}")


def read_expenses_from_csv(filepath: str):
    """
    Generator: lazily parse a CSV file into validated Expense objects, one
    row at a time. Does NOT touch the database — pairs with import_expenses_to_db
    below, or use it standalone to preview/validate a file before committing it.
    """
    if not os.path.exists(filepath):
        raise FileImportError(f"File not found: {filepath}")
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for line_number, row in enumerate(reader, start=2):  # header is line 1
                yield _parse_row(row, line_number)
    except ValidationError:
        raise
    except Exception as e:
        raise FileImportError(f"read_expenses_from_csv failed: {e}")


@log_activity
def import_expenses_to_db(db, filepath: str) -> dict:
    """
    Read a CSV and insert every valid row via db.add_expense(). Bad rows are
    skipped (not fatal) so one typo doesn't abort an entire import.
    Returns {"imported": int, "skipped": int, "errors": [str, ...]}.
    """
    imported, skipped, errors = 0, 0, []
    try:
        for expense in read_expenses_from_csv(filepath):
            try:
                db.add_expense(expense)
                imported += 1
            except Exception as e:
                skipped += 1
                errors.append(str(e))
    except ValidationError as e:
        skipped += 1
        errors.append(str(e))
    except FileImportError:
        raise

    logger.info(f"CSV import from {filepath}: {imported} imported, {skipped} skipped")
    return {"imported": imported, "skipped": skipped, "errors": errors}