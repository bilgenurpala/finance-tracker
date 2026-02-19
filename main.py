from rich.console import Console
from rich.table import Table
from src.models.database import initialize_db
from src.services.transaction_service import add_transaction, list_transactions, remove_transaction, get_monthly_summary, edit_transaction
from src.models.category import create_category, get_all_categories
from src.services.budget_service import add_budget, get_budget_status, remove_budget
from src.services.recurring_service import get_recurring_transactions, apply_recurring_transactions
from src.reports.charts import plot_monthly_summary, plot_expense_by_category, plot_monthly_trend
from src.investments.stock_tracker import add_investment, get_all_investments, delete_investment, get_portfolio_status

console = Console()

def show_menu():
    console.print("\n[bold cyan]Finance Tracker[/bold cyan]")
    console.print("1.  Add Transaction")
    console.print("2.  List Transactions")
    console.print("3.  Monthly Summary")
    console.print("4.  Add Category")
    console.print("5.  List Categories")
    console.print("6.  Add Budget Goal")
    console.print("7.  Budget Status")
    console.print("8.  Delete Transaction")
    console.print("9.  Edit Transaction")
    console.print("10. Add Recurring Transaction")
    console.print("11. List Recurring Transactions")
    console.print("12. Apply Recurring Transactions")
    console.print("13. Chart: Income vs Expense")
    console.print("14. Chart: Expenses by Category")
    console.print("15. Chart: Monthly Trend")
    console.print("16. Add Investment")
    console.print("17. Portfolio Status")
    console.print("18. Delete Investment")
    console.print("0.  Exit")

def show_transactions():
    transactions = list_transactions()
    if not transactions:
        console.print("[yellow]No transactions found.[/yellow]")
        return

    table = Table(title="Transactions")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Amount", justify="right")
    table.add_column("Recurring")

    for t in transactions:
        color = "green" if t["type"] == "income" else "red"
        table.add_row(
            str(t["id"]),
            t["date"],
            f"[{color}]{t['type']}[/{color}]",
            t["category"] or "-",
            t["description"] or "-",
            f"[{color}]{t['amount']}[/{color}]",
            "Yes" if t["is_recurring"] else "No"
        )

    console.print(table)

def show_categories():
    categories = get_all_categories()
    if not categories:
        console.print("[yellow]No categories found.[/yellow]")
        return

    table = Table(title="Categories")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Type")

    for c in categories:
        c = dict(c)
        color = "green" if c["type"] == "income" else "red"
        table.add_row(str(c["id"]), c["name"], f"[{color}]{c['type']}[/{color}]")

    console.print(table)

def input_transaction():
    try:
        amount = float(input("Amount: "))
        description = input("Description: ")
        show_categories()
        category_id = int(input("Category ID: "))
        type = input("Type (income/expense): ").strip().lower()
        date = input("Date (YYYY-MM-DD) or press Enter for today: ").strip() or None
        add_transaction(amount, description, category_id, type, date)
        console.print("[green]Transaction added successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def input_category():
    name = input("Category name: ").strip()
    type = input("Type (income/expense): ").strip().lower()
    try:
        create_category(name, type)
        console.print("[green]Category added successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def input_monthly_summary():
    month = input("Month (YYYY-MM): ").strip()
    summary = get_monthly_summary(month)
    console.print(f"\n[bold]Summary for {summary['month']}[/bold]")
    console.print(f"[green]Total Income:  {summary['total_income']}[/green]")
    console.print(f"[red]Total Expense: {summary['total_expense']}[/red]")
    console.print(f"[cyan]Balance:       {summary['balance']}[/cyan]")

def input_budget():
    show_categories()
    try:
        category_id = int(input("Category ID: "))
        amount = float(input("Budget amount: "))
        month = input("Month (YYYY-MM): ").strip()
        add_budget(category_id, amount, month)
        console.print("[green]Budget goal added successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def show_budget_status():
    month = input("Month (YYYY-MM): ").strip()
    status = get_budget_status(month)

    if not status:
        console.print("[yellow]No budget goals found for this month.[/yellow]")
        return

    table = Table(title=f"Budget Status - {month}")
    table.add_column("Category")
    table.add_column("Budget", justify="right")
    table.add_column("Spent", justify="right")
    table.add_column("Remaining", justify="right")
    table.add_column("Usage %", justify="right")

    for s in status:
        color = "green" if s["percentage"] <= 80 else "yellow" if s["percentage"] <= 100 else "red"
        table.add_row(
            s["category"],
            str(s["budget"]),
            str(s["spent"]),
            f"[{color}]{s['remaining']}[/{color}]",
            f"[{color}]{s['percentage']}%[/{color}]"
        )

    console.print(table)

def delete_transaction_input():
    show_transactions()
    try:
        transaction_id = int(input("Transaction ID to delete: "))
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm == "y":
            remove_transaction(transaction_id)
            console.print("[green]Transaction deleted successfully![/green]")
        else:
            console.print("[yellow]Cancelled.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def edit_transaction_input():
    show_transactions()
    try:
        transaction_id = int(input("Transaction ID to edit: "))
        amount = float(input("New amount: "))
        description = input("New description: ")
        show_categories()
        category_id = int(input("New category ID: "))
        type = input("New type (income/expense): ").strip().lower()
        date = input("New date (YYYY-MM-DD): ").strip()
        edit_transaction(transaction_id, amount, description, category_id, type, date)
        console.print("[green]Transaction updated successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def input_recurring_transaction():
    try:
        amount = float(input("Amount: "))
        description = input("Description: ")
        show_categories()
        category_id = int(input("Category ID: "))
        type = input("Type (income/expense): ").strip().lower()
        add_transaction(amount, description, category_id, type, is_recurring=1)
        console.print("[green]Recurring transaction added successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def show_recurring_transactions():
    transactions = get_recurring_transactions()
    if not transactions:
        console.print("[yellow]No recurring transactions found.[/yellow]")
        return

    table = Table(title="Recurring Transactions")
    table.add_column("ID", style="dim")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Amount", justify="right")

    for t in transactions:
        color = "green" if t["type"] == "income" else "red"
        table.add_row(
            str(t["id"]),
            f"[{color}]{t['type']}[/{color}]",
            t["category"] or "-",
            t["description"] or "-",
            f"[{color}]{t['amount']}[/{color}]"
        )

    console.print(table)

def input_apply_recurring():
    month = input("Month to apply recurring transactions (YYYY-MM): ").strip()
    applied = apply_recurring_transactions(month)
    if applied:
        console.print(f"[green]Applied {len(applied)} recurring transaction(s):[/green]")
        for name in applied:
            console.print(f"  - {name}")
    else:
        console.print("[yellow]No new recurring transactions to apply.[/yellow]")

def input_chart_summary():
    month = input("Month (YYYY-MM): ").strip()
    plot_monthly_summary(month)

def input_chart_category():
    month = input("Month (YYYY-MM): ").strip()
    plot_expense_by_category(month)

def input_chart_trend():
    months_input = input("Enter months separated by comma (e.g. 2024-01,2024-02,2024-03): ").strip()
    months = [m.strip() for m in months_input.split(",")]
    plot_monthly_trend(months)

def input_add_investment():
    console.print("\n[bold]Markets:[/bold] bist / nasdaq / crypto")
    try:
        symbol = input("Symbol (e.g. THYAO, AAPL, BTC): ").strip().upper()
        shares = float(input("Number of shares: "))
        buy_price = float(input("Buy price: "))
        market = input("Market (bist/nasdaq/crypto): ").strip().lower()
        add_investment(symbol, shares, buy_price, market)
        console.print("[green]Investment added successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def show_portfolio_status():
    console.print("[yellow]Fetching current prices...[/yellow]")
    portfolio = get_portfolio_status()

    if not portfolio:
        console.print("[yellow]No investments found.[/yellow]")
        return

    table = Table(title="Portfolio Status")
    table.add_column("ID", style="dim")
    table.add_column("Symbol")
    table.add_column("Market")
    table.add_column("Shares")
    table.add_column("Buy Price", justify="right")
    table.add_column("Current Price", justify="right")
    table.add_column("Total Value", justify="right")
    table.add_column("Profit/Loss", justify="right")
    table.add_column("P/L %", justify="right")

    for inv in portfolio:
        if inv["current_price"] is None:
            table.add_row(str(inv["id"]), inv["symbol"], inv["market"], str(inv["shares"]),
                          str(inv["buy_price"]), "N/A", "N/A", "N/A", "N/A")
            continue

        color = "green" if inv["profit_loss"] >= 0 else "red"
        table.add_row(
            str(inv["id"]),
            inv["symbol"],
            inv["market"],
            str(inv["shares"]),
            str(inv["buy_price"]),
            str(inv["current_price"]),
            str(inv["total_value"]),
            f"[{color}]{inv['profit_loss']}[/{color}]",
            f"[{color}]{inv['profit_loss_pct']}%[/{color}]"
        )

    console.print(table)

def delete_investment_input():
    investments = get_all_investments()
    if not investments:
        console.print("[yellow]No investments found.[/yellow]")
        return

    table = Table(title="Investments")
    table.add_column("ID", style="dim")
    table.add_column("Symbol")
    table.add_column("Market")
    table.add_column("Shares")
    table.add_column("Buy Price", justify="right")

    for inv in investments:
        table.add_row(str(inv["id"]), inv["symbol"], inv["market"], str(inv["shares"]), str(inv["buy_price"]))

    console.print(table)

    try:
        investment_id = int(input("Investment ID to delete: "))
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm == "y":
            delete_investment(investment_id)
            console.print("[green]Investment deleted successfully![/green]")
        else:
            console.print("[yellow]Cancelled.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def main():
    initialize_db()
    while True:
        show_menu()
        choice = input("\nChoice: ").strip()
        if choice == "1":
            input_transaction()
        elif choice == "2":
            show_transactions()
        elif choice == "3":
            input_monthly_summary()
        elif choice == "4":
            input_category()
        elif choice == "5":
            show_categories()
        elif choice == "6":
            input_budget()
        elif choice == "7":
            show_budget_status()
        elif choice == "8":
            delete_transaction_input()
        elif choice == "9":
            edit_transaction_input()
        elif choice == "10":
            input_recurring_transaction()
        elif choice == "11":
            show_recurring_transactions()
        elif choice == "12":
            input_apply_recurring()
        elif choice == "13":
            input_chart_summary()
        elif choice == "14":
            input_chart_category()
        elif choice == "15":
            input_chart_trend()
        elif choice == "16":
            input_add_investment()
        elif choice == "17":
            show_portfolio_status()
        elif choice == "18":
            delete_investment_input()
        elif choice == "0":
            console.print("[bold]Goodbye![/bold]")
            break
        else:
            console.print("[red]Invalid choice.[/red]")

if __name__ == "__main__":
    main()