from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date
from src.services.transaction_service import add_transaction, list_transactions, remove_transaction, get_monthly_summary, edit_transaction
from src.models.category import create_category, get_all_categories, delete_category
from src.services.budget_service import add_budget, get_budget_status
from src.investments.stock_tracker import add_investment, get_all_investments, delete_investment, get_portfolio_status

main = Blueprint("main", __name__)

@main.route("/")
def index():
    current_month = date.today().strftime("%Y-%m")
    transactions = list_transactions()
    categories = [dict(c) for c in get_all_categories()]
    summary = get_monthly_summary(current_month)
    return render_template("index.html", transactions=transactions, categories=categories, summary=summary, current_month=current_month)

@main.route("/add-transaction", methods=["POST"])
def add_transaction_route():
    amount = float(request.form["amount"])
    description = request.form["description"]
    category_id = int(request.form["category_id"])
    type = request.form["type"]
    date = request.form["date"] or None
    add_transaction(amount, description, category_id, type, date)
    return redirect(url_for("main.index"))

@main.route("/delete-transaction/<int:transaction_id>")
def delete_transaction_route(transaction_id):
    remove_transaction(transaction_id)
    return redirect(url_for("main.index"))

@main.route("/summary")
def summary():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    s = get_monthly_summary(month)
    return render_template("summary.html", summary=s, month=month)

@main.route("/budget")
def budget():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    categories = [dict(c) for c in get_all_categories()]
    status = get_budget_status(month)
    return render_template("budget.html", categories=categories, status=status, month=month)

@main.route("/add-budget", methods=["POST"])
def add_budget_route():
    category_id = int(request.form["category_id"])
    amount = float(request.form["amount"])
    month = request.form["month"]
    add_budget(category_id, amount, month)
    return redirect(url_for("main.budget"))

@main.route("/investments")
def investments():
    portfolio = get_portfolio_status()
    return render_template("investments.html", portfolio=portfolio)

@main.route("/add-investment", methods=["POST"])
def add_investment_route():
    symbol = request.form["symbol"]
    shares = float(request.form["shares"])
    buy_price = float(request.form["buy_price"])
    market = request.form["market"]
    add_investment(symbol, shares, buy_price, market)
    return redirect(url_for("main.investments"))

@main.route("/delete-investment/<int:investment_id>")
def delete_investment_route(investment_id):
    delete_investment(investment_id)
    return redirect(url_for("main.investments"))

@main.route("/categories")
def categories():
    cats = [dict(c) for c in get_all_categories()]
    return render_template("categories.html", categories=cats)

@main.route("/add-category", methods=["POST"])
def add_category_route():
    name = request.form["name"].strip()
    type = request.form["type"]
    create_category(name, type)
    return redirect(url_for("main.categories"))

@main.route("/delete-category/<int:category_id>")
def delete_category_route(category_id):
    delete_category(category_id)
    return redirect(url_for("main.categories"))