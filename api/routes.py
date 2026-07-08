from flask import Blueprint, jsonify, request

from analytics.reports import get_expenses_dataframe
from database.db_manager import DatabaseManager
from database.models import Category, Expense, Budget
from ml.predictor import predict_next_month_spend

api_bp = Blueprint("main", __name__)
db = DatabaseManager()


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@api_bp.route("/expenses", methods=["GET"])
def get_expenses():
    user_id = request.args.get("user_id", default=1, type=int)
    expenses = db.get_expenses(user_id)
    return jsonify([
        {
            "id": expense.id,
            "user_id": expense.user_id,
            "category_id": expense.category_id,
            "amount": expense.amount,
            "description": expense.description_,
            "date": expense.date_.isoformat() if expense.date_ else None,
        }
        for expense in expenses
    ])


@api_bp.route("/expenses", methods=["POST"])
def create_expense():
    payload = request.get_json(silent=True) or {}
    expense = Expense(
        user_id=payload.get("user_id", 1),
        category_id=payload.get("category_id", 1),
        amount=float(payload.get("amount", 0)),
        description_=payload.get("description", ""),
        date_=payload.get("date") or "2026-01-01",
    )
    expense_id = db.add_expense(expense)
    return jsonify({"id": expense_id, "status": "created"}), 201


@api_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = db.get_all_categories()
    return jsonify([
        {"id": category.id, "name": category.name, "budget_limit": category.budget_limit}
        for category in categories
    ])


@api_bp.route("/budgets", methods=["GET"])
def get_budgets():
    user_id = request.args.get("user_id", default=1, type=int)
    budgets = db.get_budgets(user_id)
    return jsonify([
        {
            "id": budget.id,
            "user_id": budget.user_id,
            "category_id": budget.category_id,
            "amount": budget.amount,
            "month": budget.month_,
        }
        for budget in budgets
    ])


@api_bp.route("/predict", methods=["GET"])
def predict():
    user_id = request.args.get("user_id", default=1, type=int)
    df = get_expenses_dataframe(db, user_id=user_id)
    estimate = predict_next_month_spend(df, months_ahead=1)
    return jsonify({"user_id": user_id, "estimated_next_month_spend": estimate})
