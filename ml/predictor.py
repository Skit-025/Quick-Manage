import numpy as np
import pandas as pd


def _prepare_monthly_totals(df: pd.DataFrame) -> list:
    """Return a sorted list of monthly totals from a raw expenses DataFrame."""
    if df is None or df.empty:
        return []

    required_columns = {"date_", "amount"}
    if not required_columns.issubset(set(df.columns)):
        return []

    work = df.copy()
    work["date_"] = pd.to_datetime(work["date_"], errors="coerce")
    work["amount"] = pd.to_numeric(work["amount"], errors="coerce")
    work = work.dropna(subset=["date_", "amount"])

    if work.empty:
        return []

    work["month"] = work["date_"].dt.to_period("M").astype(str)
    monthly = (
        work.groupby("month", sort=True)["amount"]
        .sum()
        .reset_index()
        .sort_values("month")
    )

    return monthly["amount"].astype(float).tolist()


def predict_next_month_spend(df: pd.DataFrame, months_ahead: int = 1) -> float:
    """Estimate the spending for the next month using a simple linear trend."""
    monthly_totals = _prepare_monthly_totals(df)
    if not monthly_totals:
        return 0.0

    if len(monthly_totals) < 2:
        return round(float(monthly_totals[-1]), 2)

    x = np.arange(len(monthly_totals))
    y = np.array(monthly_totals, dtype=float)
    slope, intercept = np.polyfit(x, y, deg=1)

    future_index = len(monthly_totals) + months_ahead - 1
    prediction = intercept + slope * future_index
    return round(float(prediction), 2)


def forecast_monthly_spend(df: pd.DataFrame, months_ahead: int = 3) -> list:
    """Return a list of future monthly spend estimates for the requested horizon."""
    if months_ahead is None or months_ahead < 1:
        return []

    monthly_totals = _prepare_monthly_totals(df)
    if not monthly_totals:
        return []

    if len(monthly_totals) < 2:
        last_value = float(monthly_totals[-1])
        return [round(last_value, 2) for _ in range(months_ahead)]

    x = np.arange(len(monthly_totals))
    y = np.array(monthly_totals, dtype=float)
    slope, intercept = np.polyfit(x, y, deg=1)

    forecasts = []
    for step in range(1, months_ahead + 1):
        future_index = len(monthly_totals) + step - 1
        prediction = intercept + slope * future_index
        forecasts.append(round(float(prediction), 2))

    return forecasts
