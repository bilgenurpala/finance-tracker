# FinTrack v1 — Security Audit Code Evidence

Captured on 2026-09-07 before the security history rewrite.

This document preserves selected source excerpts from the March 2026 version.
Secret values and historical commit object IDs are intentionally omitted.

## 1. JWT cookies without CSRF protection or expiration

Source: `web/__init__.py`, original lines 9–10.

```python
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
```

Finding: cookie-based JWT authentication had CSRF protection disabled, while
access tokens had no expiration.

What I did not know then: moving a token into a cookie does not provide CSRF
protection by itself, and authentication tokens need a bounded lifetime.

## 2. State-changing deletion routes accepted GET requests

Source: `web/routes.py`, original lines 104–108, 153–157, and 174–178.

```python
@main.route("/delete-transaction/<int:transaction_id>")
@jwt_required()
def delete_transaction_route(transaction_id):
    remove_transaction(transaction_id)
    return redirect(url_for("main.index"))
```

```python
@main.route("/delete-investment/<int:investment_id>")
@jwt_required()
def delete_investment_route(investment_id):
    delete_investment(investment_id)
    return redirect(url_for("main.investments"))
```

```python
@main.route("/delete-category/<int:category_id>")
@jwt_required()
def delete_category_route(category_id):
    delete_category(category_id)
    return redirect(url_for("main.categories"))
```

Finding: the routes omitted an explicit method, so Flask accepted GET. Reading
a URL could therefore trigger a destructive state change.

What I did not know then: GET must be safe and idempotent; destructive actions
need an appropriate mutation method plus CSRF protection.

## 3. Financial tables had no user ownership field

Source: `src/models/database.py`, original lines 26–52.

```sql
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
)
```

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    description TEXT,
    category_id INTEGER,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    date TEXT NOT NULL,
    is_recurring INTEGER DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
```

```sql
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    amount REAL NOT NULL,
    month TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
```

Finding: categories, transactions, and budgets had no `user_id`. Authentication
was added after the schema, so data ownership could not be enforced in queries.

What I did not know then: authorization has to be represented in the data model,
not added only at the route layer.

## 4. AI output was written to the DOM as HTML

Source: `web/templates/ai.html`, original lines 202–211.

```javascript
else if (/^# /.test(line))    html += line.replace(/^# (.*)/,'<h1>$1</h1>');
else if (/^> /.test(line))    html += line.replace(/^> (.*)/,'<blockquote>$1</blockquote>');
else if (/^[-*] /.test(line)) html += line.replace(/^[-*] (.*)/,'<li>$1</li>');
else if (/^\d+\. /.test(line)) html += '<li>'+line.replace(/^\d+\. /,'')+'</li>';
else if (line.trim()==='---') html += '<hr>';
else if (line.trim()==='')    html += '<br>';
else html += '<p>'+line+'</p>';

resultEl.innerHTML = html;
```

Finding: a handwritten Markdown-like renderer assembled HTML and assigned it
directly through `innerHTML` without sanitization.

What I did not know then: model output is untrusted content and must be safely
rendered or sanitized before reaching an HTML sink.

## 5. Transaction descriptions were inserted directly into the prompt

Source: `src/services/ai_service.py`, original lines 13–16 and 23–31.

```python
transactions_text = "\n".join([
    f"- {t['date']}: {t['type']} | {t['category'] or 'No category'} | {t['description']} | {t['amount']} TL"
    for t in transactions
])
```

```python
prompt = f"""You are a personal finance assistant. Analyze the following financial data for {month} and provide insights in English.

Transactions:
{transactions_text}
"""
```

Finding: user-controlled transaction descriptions were mixed directly with
instructions, without explicit boundaries, normalization, or length limits.

What I did not know then: stored application data can become indirect prompt
injection when it is later inserted into an LLM request.

## 6. Budgets were matched by category display name

Source: `src/services/budget_service.py`, original lines 14–21.

```python
for b in budgets:
    b = dict(b)
    spent = sum(
        t["amount"] for t in transactions
        if t["category"] == b["category"] and t["type"] == "expense"
    )
    remaining = b["amount"] - spent
    percentage = (spent / b["amount"]) * 100 if b["amount"] > 0 else 0
```

Finding: spending was associated with a budget through a mutable category name
instead of a stable category identifier.

What I did not know then: relationships should use stable keys; display strings
are presentation data and can change or collide.
