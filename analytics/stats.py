import numpy as np

def average_expense(amounts)->float:
    """Return the mean of a list/array of expense amounts."""
    if len(amounts)==0:
        return 0.0
    return float(np.mean(amounts))

def std_deviation(amounts)->float:
    """Return the std_deviation of expense amounts."""
    if len(amounts)==0:
        return 0.0
    return float(np.std(amounts))

def detect_trend(monthly_totals) -> float:
    """
    Fit a straight line (degree-1 polynomial) through monthly totals and
    return its slope. Positive slope = spending is trending up over time,
    negative = trending down, near zero = flat.

    monthly_totals should be a list of numbers in chronological order,
    e.g. [160.0, 290.0, 310.0] for three consecutive months.
    """
    n = len(monthly_totals)
    if n < 2:
        return 0.0  # can't detect a trend with fewer than 2 points

    x = np.arange(n)                      # [0, 1, 2, ...] representing month order
    y = np.array(monthly_totals)
    slope, intercept = np.polyfit(x, y, deg=1)
    return float(slope)


def find_anomalies(amounts, threshold: float = 2.0) -> list:
    """
    Return the amounts that are more than `threshold` standard deviations
    away from the mean — i.e. unusually large (or small) expenses.
    """
    if len(amounts) == 0:
        return []

    arr = np.array(amounts, dtype=float)
    mean = np.mean(arr)
    std = np.std(arr)

    if std == 0:
        return []  # everything is identical, nothing stands out

    z_scores = np.abs((arr - mean) / std)
    anomalies = arr[z_scores > threshold]
    return anomalies.tolist()