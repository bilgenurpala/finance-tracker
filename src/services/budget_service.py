from src.models.budget import create_budget, get_budgets_by_month, delete_budget
from src.services.transaction_service import list_transactions

def add_budget(category_id, amount, month):
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    create_budget(category_id, amount, month)

def get_budget_status(month):
    budgets = get_budgets_by_month(month)
    transactions = list_transactions(month)
    
    result = []
    for b in budgets:
        b = dict(b)
        spent = sum(
            t["amount"] for t in transactions
            if t["category"] == b["category"] and t["type"] == "expense"
        )
        remaining = b["amount"] - spent
        percentage = (spent / b["amount"]) * 100 if b["amount"] > 0 else 0
        
        result.append({
            "id": b["id"],
            "category": b["category"],
            "month": b["month"],
            "budget": b["amount"],
            "spent": spent,
            "remaining": remaining,
            "percentage": round(percentage, 1)
        })
    
    return result

def remove_budget(budget_id):
    delete_budget(budget_id)