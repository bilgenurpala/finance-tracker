import bcrypt
from src.models.database import get_connection

def create_user(username, email, password):
    """Register a new user. Returns (True, user_id) or (False, error_message)."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return True, user_id
    except Exception as e:
        error = str(e)
        if "username" in error:
            return False, "Username already taken."
        elif "email" in error:
            return False, "Email already registered."
        return False, "Registration failed."
    finally:
        conn.close()

def verify_user(username, password):
    """Login check. Returns user dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return dict(user)
    return None

def get_user_by_id(user_id):
    """Get user by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None