import pandas as pd

def get_expenses_dataframe(db,user_id:int)->pd.DataFrame:
    """
    Fetch a user's expenses from the DB and load them into a DataFrame.
    Columns: id, user_id, category_id, amount, description_, date_
    """
    expenses=db.get_expenses(user_id)


    # Convert each Expense dataclass object into a plain dict, then build the DataFrame
    rows=[
        {
            "id":e.id,
            "user_id": e.user_id,
            "category_id": e.category_id,
            "amount": e.amount,
            "description_": e.description_,
            "date_": e.date_,
        }
        for e in expenses
    ]
    df=pd.DataFrame(rows)

    if not df.empty:
        df["date_"]=pd.to_datetime(df['date_']) # so that it could be group by month later
    return df

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return total amount spent per month (YYYY-MM)."""
    if df.empty:
        return pd.DataFrame(columns=["month", "total_amount"]).set_index("month")

    df = df.copy()
    df["month"] = df["date_"].dt.strftime("%Y-%m")

    summary = df.groupby("month")["amount"].sum().reset_index()
    summary = summary.rename(columns={"amount": "total_amount"})
    return summary.set_index("month")


def category_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Return total amount spent per category_id."""
    if df.empty:
        return pd.DataFrame(columns=["category_id", "total_amount"])

    totals = df.groupby("category_id")["amount"].sum().reset_index()
    totals = totals.rename(columns={"amount": "total_amount"})
    return totals


def top_spending_category(df: pd.DataFrame):
    """Return (category_id, total_amount) for the single highest-spending category."""
    totals = category_totals(df)
    if totals.empty:
        return None, 0.0

    top_row = totals.loc[totals["total_amount"].idxmax()]
    return int(top_row["category_id"]), float(top_row["total_amount"])
