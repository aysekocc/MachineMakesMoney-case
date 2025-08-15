
import hashlib

from django.db import models
from django.conf import settings

class ImportBatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    row_count = models.IntegerField(default=0)
    inserted_count = models.IntegerField(default=0)
    error_summary = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3)
    type = models.CharField(max_length=6)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    unique_hash = models.CharField(max_length=64, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','unique_hash'], name='uniq_user_uniquehash')
        ]

    @staticmethod
    def make_hash(user_id, date, amount, currency, description):
        key = f"{user_id}|{date}|{amount}|{currency}|{description}".encode('utf-8')
        return hashlib.sha256(key).hexdigest()