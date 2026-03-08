# 💰 FinTrack

> A full-stack personal finance management application with a professional dark SaaS dashboard, JWT authentication, AI-powered insights, and real-time investment tracking.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Claude AI](https://img.shields.io/badge/AI-Claude%20API-orange?logo=anthropic)
![JWT](https://img.shields.io/badge/Auth-JWT-green?logo=jsonwebtokens)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)

---

## 🔍 Overview

FinTrack is a personal finance application that helps you manage income, expenses, budgets, and investments in one place. It features a professional dark-themed SaaS dashboard with interactive Chart.js visualizations, JWT-based user authentication, and an AI assistant powered by the Claude API for spending analysis, savings tips, and natural language transaction parsing.

---

## 📸 Screenshots

### Dashboard
![Dashboard](web/static/screenshots/dashboard.png)

### Analytics
![Analytics](web/static/screenshots/analytics.png)

### Budget
![Budget](web/static/screenshots/budget.png)

### Investments
![Investments](web/static/screenshots/investments.png)

### Categories
![Categories](web/static/screenshots/categories.png)

### AI Assistant
![AI Assistant](web/static/screenshots/ai-assistant.png)

### AI Spending Analysis
![AI Analysis](web/static/screenshots/ai-analysis.png)

### AI Savings Tips
![AI Savings](web/static/screenshots/ai-savings.png)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Authentication | JWT-based register, login and logout with bcrypt password hashing |
| 💸 Transactions | Add, edit, delete income & expense records |
| 🗂️ Categories | Organize transactions by custom categories |
| 🎯 Budget Goals | Set monthly spending limits with progress tracking |
| 📊 Charts | Interactive Chart.js visualizations across all pages |
| 📈 Investments | Track BIST, NYSE/NASDAQ and crypto portfolios in real-time |
| 🤖 AI Assistant | Claude-powered spending analysis, savings tips & natural language input |
| 💬 Natural Language | Add transactions by typing plain text ("spent 150 TL on groceries") |
| 🌐 Landing Page | Professional marketing page with hero, features and screenshots |

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
│   │   ├── recurring_service.py
│   │   ├── auth_service.py
│   │   └── ai_service.py
│   ├── reports/
│   │   └── charts.py
│   └── investments/
│       └── stock_tracker.py
├── web/
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── index.html
│   │   ├── summary.html
│   │   ├── budget.html
│   │   ├── investments.html
│   │   ├── categories.html
│   │   └── ai.html
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── screenshots/
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

**3. Configure API key**

Create a `config.py` file in the root directory:
```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "data", "finance.db")
CURRENCY = "TL"
SECRET_KEY = "your-secret-key-here"
ANTHROPIC_API_KEY = "your-api-key-here"  # Get from console.anthropic.com
```

**4. Run the application**
```bash
py app.py
```
Then open http://127.0.0.1:5000 in your browser.

---

## 🚀 Usage

### Getting Started
1. Navigate to `http://127.0.0.1:5000`
2. Click **Get Started** to create an account
3. Log in and access your personal dashboard

### Web Dashboard
Use the sidebar to navigate all features:

- **Dashboard** — Monthly stats, income vs expense chart, category breakdown
- **Analytics** — Monthly summary with interactive charts
- **Budget** — Set and track budget goals with progress bars and charts
- **Investments** — Add and track BIST, NYSE/NASDAQ, and crypto portfolios with P&L charts
- **Categories** — Manage income and expense categories
- **AI Assistant** — Claude-powered spending analysis, savings tips, and natural language transaction input

### AI Assistant
Navigate to `/ai` to use AI features:
- **Spending Analysis** — Detailed monthly breakdown with insights
- **Savings Tips** — Personalized recommendations based on your data
- **Natural Language Input** — Type transactions in plain text:
  - `"spent 200 TL on groceries today"`
  - `"received 5000 TL salary"`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| Flask | Web framework |
| SQLite | Local database |
| Flask-JWT-Extended | JWT authentication |
| bcrypt | Password hashing |
| Jinja2 | HTML templating |
| Chart.js | Interactive charts |
| Claude API | AI spending analysis & NLP |
| Anthropic SDK | Claude API client |
| yfinance | Real-time stock & crypto prices |
| Rich | Terminal UI |
| Matplotlib | Terminal charts |

---

## 🗺️ Roadmap

- [x] Terminal application
- [x] Flask web interface
- [x] Professional dark SaaS dashboard
- [x] Interactive Chart.js visualizations
- [x] Real-time investment tracking with P&L
- [x] AI-powered spending analysis (Claude API)
- [x] Natural language transaction input
- [x] Landing page
- [x] User authentication (JWT + bcrypt)
- [ ] Multi-currency support
- [ ] Export to CSV/PDF

---

## 📄 License

This project is licensed under the MIT License.