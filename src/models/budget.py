from src.models.database import get_connection

def create_budget(category_id, amount, month):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO budgets (category_id, amount, month) VALUES (?, ?, ?)",
        (category_id, amount, month)
    )
    conn.commit()
    conn.close()

def get_budgets_by_month(month):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, b.amount, b.month, c.name as category
        FROM budgets b
        LEFT JOIN categories c ON b.category_id = c.id
        WHERE b.month = ?
    """, (month,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_budget(budget_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    conn.commit()
    conn.close()