from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Transaction
import json
import os

@shared_task
def generate_weekly_reports():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    users = Transaction.objects.values_list("user", flat=True).distinct()
    reports_dir = os.path.join("reports", "weekly")
    os.makedirs(reports_dir, exist_ok=True)

    for user_id in users:
        transactions = Transaction.objects.filter(
            user_id=user_id, date__range=[start_date, end_date]
        )
        total_income = sum(t.amount for t in transactions if t.type == "credit")
        total_expense = sum(abs(t.amount) for t in transactions if t.type == "debit")
        net_cash_flow = total_income - total_expense

        report = {
            "user_id": user_id,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "total_income": total_income,
            "total_expense": total_expense,
            "net_cash_flow": net_cash_flow,
        }

        file_path = os.path.join(reports_dir, f"user_{user_id}_{end_date}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
