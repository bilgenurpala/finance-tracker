import matplotlib.pyplot as plt
from src.services.transaction_service import list_transactions, get_monthly_summary

def plot_monthly_summary(month):
    summary = get_monthly_summary(month)
    
    labels = ["Income", "Expense"]
    values = [summary["total_income"], summary["total_expense"]]
    colors = ["#2ecc71", "#e74c3c"]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=colors, width=0.4)
    
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 f"{value:.0f}", ha="center", fontsize=11)
    
    plt.title(f"Income vs Expense - {month}")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(f"data/summary_{month}.png")
    plt.show()
    print(f"Chart saved: data/summary_{month}.png")

def plot_expense_by_category(month):
    transactions = list_transactions(month)
    expenses = [t for t in transactions if t["type"] == "expense"]
    
    if not expenses:
        print("No expense data found.")
        return
    
    category_totals = {}
    for t in expenses:
        category = t["category"] or "Other"
        category_totals[category] = category_totals.get(category, 0) + t["amount"]
    
    labels = list(category_totals.keys())
    values = list(category_totals.values())
    
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Expenses by Category - {month}")
    plt.tight_layout()
    plt.savefig(f"data/expenses_{month}.png")
    plt.show()
    print(f"Chart saved: data/expenses_{month}.png")

def plot_monthly_trend(months):
    incomes = []
    expenses = []
    
    for month in months:
        summary = get_monthly_summary(month)
        incomes.append(summary["total_income"])
        expenses.append(summary["total_expense"])
    
    plt.figure(figsize=(10, 5))
    plt.plot(months, incomes, marker="o", color="#2ecc71", label="Income")
    plt.plot(months, expenses, marker="o", color="#e74c3c", label="Expense")
    plt.title("Monthly Trend")
    plt.ylabel("Amount")
    plt.xlabel("Month")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/trend.png")
    plt.show()
    print("Chart saved: data/trend.png")