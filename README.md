# 💰 Finance Tracker

> A Python-based personal finance management application with investment portfolio tracking.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)

---

## 🔍 Overview

Finance Tracker is a terminal-based personal finance application that helps you manage your income, expenses, budgets, and investments in one place. It supports real-time stock and cryptocurrency price tracking via Yahoo Finance API.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💸 Transactions | Add, edit, delete income & expense records |
| 🗂️ Categories | Organize transactions by custom categories |
| 🎯 Budget Goals | Set monthly spending limits per category |
| 🔁 Recurring | Automate fixed monthly transactions |
| 📊 Charts | Visualize income, expenses and trends |
| 📈 Investments | Track BIST, NASDAQ and crypto portfolios |

---

## 📁 Project Structure
```
finance-tracker/
├── data/
│   └── finance.db
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── budget.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transaction_service.py
│   │   ├── budget_service.py
│   │   └── recurring_service.py
│   ├── reports/
│   │   ├── __init__.py
│   │   └── charts.py
│   └── investments/
│       ├── __init__.py
│       └── stock_tracker.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

**2. Install dependencies**
```bash
py -m pip install -r requirements.txt
```

**3. Run the application**
```bash
py main.py
```

---

## 🚀 Usage

After launching the app, navigate using the numbered menu:
```
Finance Tracker
1.  Add Transaction
2.  List Transactions
3.  Monthly Summary
4.  Add Category
5.  List Categories
6.  Add Budget Goal
7.  Budget Status
8.  Delete Transaction
9.  Edit Transaction
10. Add Recurring Transaction
11. List Recurring Transactions
12. Apply Recurring Transactions
13. Chart: Income vs Expense
14. Chart: Expenses by Category
15. Chart: Monthly Trend
16. Add Investment
17. Portfolio Status
18. Delete Investment
0.  Exit
```

**Example: Adding an investment**
```
Choice: 16
Symbol: THYAO
Shares: 10
Buy price: 150.0
Market: bist
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| SQLite | Local database |
| Rich | Terminal UI |
| Matplotlib | Charts & graphs |
| yfinance | Stock & crypto prices |

---

## 🗺️ Roadmap

- [x] Terminal application
- [ ] Flask web interface
- [ ] Django + React frontend
- [ ] Multi-currency support
- [ ] Export to CSV/PDF
- [ ] User authentication

---

## 📄 License

This project is licensed under the MIT License.