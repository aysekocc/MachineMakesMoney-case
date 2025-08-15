
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    unique_hash = serializers.CharField(read_only=True)
    category = serializers.CharField(required=False)
    class Meta:
        model = Transaction
        fields = ['id','date','amount','currency','type','description','category','unique_hash']


