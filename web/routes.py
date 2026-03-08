from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from datetime import date
from src.services.transaction_service import add_transaction, list_transactions, remove_transaction, get_monthly_summary, edit_transaction
from src.models.category import create_category, get_all_categories, delete_category
from src.services.budget_service import add_budget, get_budget_status
from src.investments.stock_tracker import add_investment, get_all_investments, delete_investment, get_portfolio_status
from src.services.ai_service import analyze_spending, parse_natural_language_transaction, get_savings_tips
from src.services.auth_service import create_user, verify_user, get_user_by_id

main = Blueprint("main", __name__)

def current_user():
    """Helper to get current user from JWT identity."""
    try:
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        return get_user_by_id(int(user_id)) if user_id else None
    except Exception:
        return None

# ── AUTH ROUTES ──────────────────────────────────────────────

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if not username or not email or not password:
        return render_template("register.html", error="All fields are required.")

    if password != confirm:
        return render_template("register.html", error="Passwords do not match.")

    if len(password) < 6:
        return render_template("register.html", error="Password must be at least 6 characters.")

    success, result = create_user(username, email, password)
    if not success:
        return render_template("register.html", error=result)

    token = create_access_token(identity=str(result))
    response = redirect(url_for("main.index"))
    set_access_cookies(response, token)
    return response

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = verify_user(username, password)
    if not user:
        return render_template("login.html", error="Invalid username or password.")

    token = create_access_token(identity=str(user["id"]))
    response = redirect(url_for("main.index"))
    set_access_cookies(response, token)
    return response

@main.route("/logout")
def logout():
    response = redirect(url_for("main.landing"))
    unset_jwt_cookies(response)
    return response

# ── PUBLIC ROUTES ─────────────────────────────────────────────

@main.route("/")
def landing():
    return render_template("landing.html")

# ── PROTECTED ROUTES ──────────────────────────────────────────

@main.route("/dashboard")
@jwt_required()
def index():
    user = current_user()
    current_month = date.today().strftime("%Y-%m")
    transactions = list_transactions()
    categories = [dict(c) for c in get_all_categories()]
    summary = get_monthly_summary(current_month)
    return render_template("index.html", transactions=transactions, categories=categories, summary=summary, current_month=current_month, user=user)

@main.route("/add-transaction", methods=["POST"])
@jwt_required()
def add_transaction_route():
    amount = float(request.form["amount"])
    description = request.form["description"]
    category_id = int(request.form["category_id"])
    type = request.form["type"]
    date = request.form["date"] or None
    add_transaction(amount, description, category_id, type, date)
    return redirect(url_for("main.index"))

@main.route("/delete-transaction/<int:transaction_id>")
@jwt_required()
def delete_transaction_route(transaction_id):
    remove_transaction(transaction_id)
    return redirect(url_for("main.index"))

@main.route("/summary")
@jwt_required()
def summary():
    user = current_user()
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    s = get_monthly_summary(month)
    return render_template("summary.html", summary=s, month=month, user=user)

@main.route("/budget")
@jwt_required()
def budget():
    user = current_user()
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    categories = [dict(c) for c in get_all_categories()]
    status = get_budget_status(month)
    return render_template("budget.html", categories=categories, status=status, month=month, user=user)

@main.route("/add-budget", methods=["POST"])
@jwt_required()
def add_budget_route():
    category_id = int(request.form["category_id"])
    amount = float(request.form["amount"])
    month = request.form["month"]
    add_budget(category_id, amount, month)
    return redirect(url_for("main.budget"))

@main.route("/investments")
@jwt_required()
def investments():
    user = current_user()
    portfolio = get_portfolio_status()
    return render_template("investments.html", portfolio=portfolio, user=user)

@main.route("/add-investment", methods=["POST"])
@jwt_required()
def add_investment_route():
    symbol = request.form["symbol"]
    shares = float(request.form["shares"])
    buy_price = float(request.form["buy_price"])
    market = request.form["market"]
    add_investment(symbol, shares, buy_price, market)
    return redirect(url_for("main.investments"))

@main.route("/delete-investment/<int:investment_id>")
@jwt_required()
def delete_investment_route(investment_id):
    delete_investment(investment_id)
    return redirect(url_for("main.investments"))

@main.route("/categories")
@jwt_required()
def categories():
    user = current_user()
    cats = [dict(c) for c in get_all_categories()]
    return render_template("categories.html", categories=cats, user=user)

@main.route("/add-category", methods=["POST"])
@jwt_required()
def add_category_route():
    name = request.form["name"].strip()
    type = request.form["type"]
    create_category(name, type)
    return redirect(url_for("main.categories"))

@main.route("/delete-category/<int:category_id>")
@jwt_required()
def delete_category_route(category_id):
    delete_category(category_id)
    return redirect(url_for("main.categories"))

@main.route("/ai")
@jwt_required()
def ai():
    user = current_user()
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    categories = [dict(c) for c in get_all_categories()]
    return render_template("ai.html", month=month, categories=categories, user=user)

@main.route("/ai/analyze", methods=["POST"])
@jwt_required()
def ai_analyze():
    month = request.form["month"]
    try:
        analysis = analyze_spending(month)
        return jsonify({"success": True, "result": analysis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@main.route("/ai/savings", methods=["POST"])
@jwt_required()
def ai_savings():
    month = request.form["month"]
    try:
        tips = get_savings_tips(month)
        return jsonify({"success": True, "result": tips})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@main.route("/ai/parse-transaction", methods=["POST"])
@jwt_required()
def ai_parse_transaction():
    text = request.json.get("text", "")
    try:
        result = parse_natural_language_transaction(text)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})