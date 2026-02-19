from src.models.database import get_connection

def create_transaction(amount, description, category_id, type, date, is_recurring=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (amount, description, category_id, type, date, is_recurring) VALUES (?, ?, ?, ?, ?, ?)",
        (amount, description, category_id, type, date, is_recurring)
    )
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.amount, t.description, t.type, t.date, t.is_recurring, c.name as category
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_transactions_by_month(month):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.amount, t.description, t.type, t.date, t.is_recurring, c.name as category
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.date LIKE ?
        ORDER BY t.date DESC
    """, (f"{month}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

def update_transaction(transaction_id, amount, description, category_id, type, date, is_recurring):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount = ?, description = ?, category_id = ?, type = ?, date = ?, is_recurring = ?
        WHERE id = ?
    """, (amount, description, category_id, type, date, is_recurring, transaction_id))
    conn.commit()
    conn.close()