import anthropic
import config
from src.services.transaction_service import list_transactions, get_monthly_summary
from src.services.budget_service import get_budget_status

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

def analyze_spending(month):
    summary = get_monthly_summary(month)
    transactions = list_transactions(month)
    budget_status = get_budget_status(month)

    transactions_text = "\n".join([
        f"- {t['date']}: {t['type']} | {t['category'] or 'No category'} | {t['description']} | {t['amount']} TL"
        for t in transactions
    ])

    budget_text = "\n".join([
        f"- {b['category']}: budget {b['budget']} TL, spent {b['spent']} TL, remaining {b['remaining']} TL ({b['percentage']}%)"
        for b in budget_status
    ]) if budget_status else "No budget goals set."

    prompt = f"""You are a personal finance assistant. Analyze the following financial data for {month} and provide insights in English.

Monthly Summary:
- Total Income: {summary['total_income']} TL
- Total Expense: {summary['total_expense']} TL
- Balance: {summary['balance']} TL

Transactions:
{transactions_text}

Budget Status:
{budget_text}

Please provide:
1. A brief spending analysis
2. Which categories have the highest expenses
3. Budget warnings if any category is over 80%
4. 3 specific saving tips based on the data

Formatting rules:
- Use # for the report title
- Use ## for main sections (1. Spending Analysis, 2. Top Expenses, 3. Budget Warnings, 4. Savings Tips)
- Use ### for subsections within each section
- Keep it concise and practical.
- Always respond in English."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def parse_natural_language_transaction(text):
    prompt = f"""Extract transaction details from this text and return ONLY a JSON object.

Text: "{text}"

Return exactly this JSON format, nothing else:
{{
    "amount": <number>,
    "description": "<short english description>",
    "type": "<income or expense>",
    "date": "<YYYY-MM-DD or null>"
}}

Rules:
- type is "expense" unless clearly stated as income
- date is null if not mentioned
- amount must be a number
- description must be in English"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    response_text = message.content[0].text.strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    return json.loads(response_text)


def get_savings_tips(month):
    summary = get_monthly_summary(month)
    budget_status = get_budget_status(month)

    over_budget = [b for b in budget_status if b['percentage'] > 80]
    over_budget_text = "\n".join([
        f"- {b['category']}: {b['percentage']}% used"
        for b in over_budget
    ]) if over_budget else "No categories over budget."

    prompt = f"""You are a personal finance assistant. Based on this data, give savings advice in English.

Month: {month}
Income: {summary['total_income']} TL
Expense: {summary['total_expense']} TL
Balance: {summary['balance']} TL

Categories over 80% budget:
{over_budget_text}

Give 3 short, specific, actionable savings tips. Be direct and practical.

Formatting rules:
- Use # for the main title
- Use ## for each tip (## 1. Tip Title)
- Use ### for any subsections within a tip
- Always respond in English."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text