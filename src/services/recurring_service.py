from src.models.transaction import get_all_transactions, create_transaction
from datetime import date, datetime

def get_recurring_transactions():
    transactions = get_all_transactions()
    return [dict(t) for t in transactions if t["is_recurring"] == 1]

def apply_recurring_transactions(month):
    recurring = get_recurring_transactions()
    existing = get_all_transactions()
    existing_dicts = [dict(t) for t in existing]
    
    applied = []
    for t in recurring:
        target_date = f"{month}-01"
        
        already_exists = any(
            e["description"] == t["description"] and
            e["date"].startswith(month)
            for e in existing_dicts
        )
        
        if not already_exists:
            create_transaction(
                t["amount"],
                t["description"],
                None,
                t["type"],
                target_date,
                is_recurring=0
            )
            applied.append(t["description"])
    
    return applied