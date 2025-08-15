
from django.contrib import admin
from .models import Transaction, ImportBatch

@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'row_count', 'inserted_count', 'created_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'amount', 'currency', 'description', 'type']
    list_filter = ['user', 'currency', 'type']
    search_fields = ['description']
