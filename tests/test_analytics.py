# Testing reports.py
# check_reports.py — temporary script, just to verify reports.py works
from database.db_manager import DatabaseManager
from analytics.reports import get_expenses_dataframe, monthly_summary, category_totals

db = DatabaseManager()
df = get_expenses_dataframe(db, user_id=1)

print(monthly_summary(df))
print(category_totals(df))


# Checking stats
from analytics.stats import average_expense, std_deviation, detect_trend, find_anomalies

amounts = [100, 60, 250, 40]
print("Average:", average_expense(amounts))
print("Std dev:", std_deviation(amounts))
print("Trend:", detect_trend([160.0, 290.0]))
print("Anomalies:", find_anomalies(amounts, threshold=1.0))

# checking charts and visualizing

from analytics.reports import get_expenses_dataframe, monthly_summary, category_totals
from analytics.charts import plot_monthly_trend, plot_category_pie, plot_category_heatmap

df = get_expenses_dataframe(db, user_id=1)

plot_monthly_trend(monthly_summary(df), "exports/reports/monthly_trend.png")
plot_category_pie(category_totals(df), "exports/reports/category_pie.png")
plot_category_heatmap(df, "exports/reports/category_heatmap.png")