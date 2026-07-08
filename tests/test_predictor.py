import pandas as pd

from ml.predictor import forecast_monthly_spend, predict_next_month_spend


def test_predict_next_month_spend_uses_linear_trend():
    df = pd.DataFrame(
        {
            "date_": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
            "amount": [100.0, 200.0, 300.0],
        }
    )

    result = predict_next_month_spend(df, months_ahead=1)

    assert result == 400.0


def test_forecast_monthly_spend_returns_requested_horizon():
    df = pd.DataFrame(
        {
            "date_": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
            "amount": [100.0, 200.0, 300.0],
        }
    )

    forecast = forecast_monthly_spend(df, months_ahead=3)

    assert len(forecast) == 3
    assert forecast[0] == 400.0
    assert forecast[-1] == 600.0


def test_empty_dataframe_returns_zero_prediction():
    df = pd.DataFrame(columns=["date_", "amount"])

    assert predict_next_month_spend(df) == 0.0
    assert forecast_monthly_spend(df, months_ahead=2) == []
