"""
analytics/charts.py — Module 3: Analytics
--------------------------------------------
PURPOSE:
    Turn the DataFrames from reports.py into visuals:
        1. plot_monthly_trend    -> bar chart of total spend per month
        2. plot_category_pie     -> pie chart of spend split across categories
        3. plot_category_heatmap -> heatmap of spend by day-of-week vs category

    Every function returns the matplotlib Figure (so Streamlit can embed it
    directly in Module 4) and optionally saves it to disk if save_path is given.

TARGET OUTPUT (example):
    plot_monthly_trend(monthly_summary_df, "exports/reports/monthly_trend.png")
    -> bar chart with months on x-axis, total_amount on y-axis, saved to disk

    plot_category_pie(category_totals_df, "exports/reports/category_pie.png")
    -> pie chart, one slice per category_id, sized by total_amount

    plot_category_heatmap(raw_df, "exports/reports/category_heatmap.png")
    -> grid: rows = day of week, columns = category_id, color = total spent
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def _save_if_needed(fig, save_path: str = None):
    """Shared helper: save the figure to disk if a path was given."""
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")
        print(f"Saved: {save_path}")


def plot_monthly_trend(monthly_df: pd.DataFrame, save_path: str = None):
    """
    Bar chart of total spend per month.
    monthly_df is expected to look like the output of reports.monthly_summary()
    — index = month (YYYY-MM), one column: total_amount.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(monthly_df.index.astype(str), monthly_df["total_amount"], color="#4C72B0")
    ax.set_title("Monthly Expense Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spent")
    plt.xticks(rotation=45)
    fig.tight_layout()

    _save_if_needed(fig, save_path)
    return fig


def plot_category_pie(category_df: pd.DataFrame, save_path: str = None):
    """
    Pie chart of spend split across categories.
    category_df is expected to look like the output of reports.category_totals()
    — columns: category_id, total_amount.
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    labels = [f"Category {cid}" for cid in category_df["category_id"]]
    ax.pie(category_df["total_amount"], labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending by Category")

    _save_if_needed(fig, save_path)
    return fig


def plot_category_heatmap(df: pd.DataFrame, save_path: str = None):
    """
    Heatmap of spend by day-of-week vs category.
    df is expected to look like the output of reports.get_expenses_dataframe()
    — raw rows with columns: category_id, amount, date_ (already datetime).
    """
    if df.empty:
        raise ValueError("Cannot build a heatmap from an empty DataFrame")

    df = df.copy()
    df["day_of_week"] = df["date_"].dt.day_name()

    pivot = df.pivot_table(
        index="day_of_week",
        columns="category_id",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    # keep days in Mon->Sun order instead of whatever order pivot_table returns
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Spending Heatmap: Day of Week vs Category")

    _save_if_needed(fig, save_path)
    return fig