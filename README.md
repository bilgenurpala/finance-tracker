# 💰 FinTrack

> A Python-based personal finance management application with a modern web dashboard and real-time investment portfolio tracking.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey?logo=flask)
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

FinTrack is a personal finance application that helps you manage income, expenses, budgets, and investments in one place. It started as a terminal-based application and evolved into a modern dark-themed web dashboard. It supports real-time stock and cryptocurrency price tracking via Yahoo Finance API.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💸 Transactions | Add, edit, delete income & expense records |
| 🗂️ Categories | Organize transactions by custom categories |
| 🎯 Budget Goals | Set monthly spending limits per category |
| 🔁 Recurring | Automate fixed monthly transactions |
| 📊 Charts | Visualize income, expenses and trends |
| 📈 Investments | Track BIST, NASDAQ and crypto portfolios in real-time |
| 🌐 Web Dashboard | Modern dark-themed web interface |

---

## 📁 Project Structure
```
finance-tracker/
├── data/
│   └── finance.db
├── src/
│   ├── models/
│   │   ├── database.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── budget.py
│   ├── services/
│   │   ├── transaction_service.py
│   │   ├── budget_service.py
│   │   └── recurring_service.py
│   ├── reports/
│   │   └── charts.py
│   └── investments/
│       └── stock_tracker.py
├── web/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── summary.html
│   │   ├── budget.html
│   │   ├── investments.html
│   │   └── categories.html
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   ├── __init__.py
│   └── routes.py
├── app.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/bilgenurpala/finance-tracker.git
cd finance-tracker
```

**2. Install dependencies**
```bash
py -m pip install -r requirements.txt
```

**3a. Run the web application**
```bash
py app.py
```
Then open http://127.0.0.1:5000 in your browser.

**3b. Run the terminal application**
```bash
py main.py
```

---

## 🚀 Usage

### Web Dashboard
After launching `app.py`, navigate to `http://127.0.0.1:5000` and use the sidebar to access all features:

- **Transactions** — View monthly stats, add and delete transactions
- **Summary** — Monthly income/expense breakdown
- **Budget** — Set and track budget goals with progress bars
- **Investments** — Add and track BIST, NASDAQ, and crypto portfolios
- **Categories** — Manage income and expense categories

### Terminal App
After launching `main.py`, use the numbered menu:
```
1.  Add Transaction          10. Add Recurring Transaction
2.  List Transactions        11. List Recurring Transactions
3.  Monthly Summary          12. Apply Recurring Transactions
4.  Add Category             13. Chart: Income vs Expense
5.  List Categories          14. Chart: Expenses by Category
6.  Add Budget Goal          15. Chart: Monthly Trend
7.  Budget Status            16. Add Investment
8.  Delete Transaction       17. Portfolio Status
9.  Edit Transaction         18. Delete Investment
0.  Exit
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| SQLite | Local database |
| Flask | Web framework |
| Jinja2 | HTML templating |
| Rich | Terminal UI |
| Matplotlib | Charts & graphs |
| yfinance | Real-time stock & crypto prices |

---

## 🗺️ Roadmap

- [x] Terminal application
- [x] Flask web interface
- [x] Dark theme dashboard
- [x] Real-time investment tracking
- [ ] Django + React frontend
- [ ] Multi-currency support
- [ ] Export to CSV/PDF
- [ ] User authentication

---

## 📄 License

This project is licensed under the MIT License.