import yfinance as yf
from src.models.database import get_connection

def add_investment(symbol, shares, buy_price, market):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            shares REAL NOT NULL,
            buy_price REAL NOT NULL,
            market TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO investments (symbol, shares, buy_price, market) VALUES (?, ?, ?, ?)",
        (symbol.upper(), shares, buy_price, market)
    )
    conn.commit()
    conn.close()

def get_all_investments():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM investments")
        rows = cursor.fetchall()
    except Exception:
        rows = []
    conn.close()
    return [dict(row) for row in rows]

def delete_investment(investment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM investments WHERE id = ?", (investment_id,))
    conn.commit()
    conn.close()

def get_current_price(symbol, market):
    try:
        if market == "bist":
            ticker = yf.Ticker(f"{symbol}.IS")
        elif market == "crypto":
            ticker = yf.Ticker(f"{symbol}-USD")
        else:
            ticker = yf.Ticker(symbol)
        
        data = ticker.fast_info
        return round(data.last_price, 2)
    except Exception:
        return None

def get_portfolio_status():
    investments = get_all_investments()
    result = []

    for inv in investments:
        current_price = get_current_price(inv["symbol"], inv["market"])
        if current_price is None:
            result.append({**inv, "current_price": None, "total_value": None, "profit_loss": None, "profit_loss_pct": None})
            continue

        total_cost = inv["shares"] * inv["buy_price"]
        total_value = inv["shares"] * current_price
        profit_loss = total_value - total_cost
        profit_loss_pct = (profit_loss / total_cost) * 100

        result.append({
            **inv,
            "current_price": current_price,
            "total_value": round(total_value, 2),
            "profit_loss": round(profit_loss, 2),
            "profit_loss_pct": round(profit_loss_pct, 2)
        })

    return result