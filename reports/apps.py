
from django.apps import AppConfig
# transactions/apps.py
from django.apps import AppConfig

class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'  # ya da 'backend.transactions' gibi proje yapınıza göre

class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
