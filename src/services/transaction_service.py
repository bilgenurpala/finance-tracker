from src.models.transaction import create_transaction, get_all_transactions, get_transactions_by_month, delete_transaction, update_transaction
from datetime import date

def add_transaction(amount, description, category_id, type, transaction_date=None, is_recurring=0):
    if transaction_date is None:
        transaction_date = str(date.today())
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    if type not in ("income", "expense"):
        raise ValueError("Type must be 'income' or 'expense'")
    create_transaction(amount, description, category_id, type, transaction_date, is_recurring)

def list_transactions(month=None):
    if month:
        rows = get_transactions_by_month(month)
    else:
        rows = get_all_transactions()
    return [dict(row) for row in rows]

def remove_transaction(transaction_id):
    delete_transaction(transaction_id)

def get_monthly_summary(month):
    transactions = list_transactions(month)
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    return {
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }

def edit_transaction(transaction_id, amount, description, category_id, type, date, is_recurring=0):
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    if type not in ("income", "expense"):
        raise ValueError("Type must be 'income' or 'expense'")
    update_transaction(transaction_id, amount, description, category_id, type, date, is_recurring)