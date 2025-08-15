# tests/test_api.py
import io
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()

@pytest.fixture
def api_client(db):
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(email="test@example.com", password="pass1234"):
        user = User.objects.create_user(username=email, email=email, password=password)
        return user
    return make_user
@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()

    api_client.force_authenticate(user=user)
    return api_client, user

# -----------------------
# Register / Login tests
# -----------------------
def test_register_user(api_client):
    data = {'email': 'newuser@example.com', 'password': 'newpass123'}
    response = api_client.post(reverse('register'), data, format='json')
    assert response.status_code == 201
    assert User.objects.filter(email='newuser@example.com').exists()

def test_login_user(api_client, create_user):
    user = create_user(email='loginuser@example.com', password='pass1234')
    response = api_client.post(reverse('login'), {'email': user.email, 'password': 'pass1234'}, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

# -----------------------
# Transaction Upload tests
# -----------------------
CSV_SAMPLE = """date,amount,currency,type,description
2025-08-01,100,TRY,credit,Satış geliri
2025-08-02,50,TRY,debit,Kira ödeme
"""

@patch('transactions.views.requests.get')
def test_transaction_upload(mock_get, auth_client):
    mock_get.return_value.json.return_value = {'rates': {'TRY': 1}}  # Döviz dönüşümü mock
    client, user = auth_client

    csv_file = io.StringIO(CSV_SAMPLE)
    csv_file.name = "sample.csv"
    response = client.post(reverse('transactions-upload'), {'file': csv_file}, format='multipart')
    assert response.status_code == 201
    assert Transaction.objects.filter(user=user).count() == 2

# -----------------------
# Transaction List tests
# -----------------------
def test_transaction_list(auth_client):
    client, user = auth_client
    # Önce veri ekle
    Transaction.objects.create(user=user, date='2025-08-01', amount=100, currency='TRY', type='credit', description='Satış', category='Gelir', unique_hash='hash1')
    Transaction.objects.create(user=user, date='2025-08-02', amount=50, currency='TRY', type='debit', description='Kira', category='Kira Gideri', unique_hash='hash2')

    response = client.get(reverse('transactions-list'))
    assert response.status_code == 200
    assert response.data['count'] == 2

# -----------------------
# Reports Summary tests
# -----------------------
def test_summary_report(auth_client):
    client, user = auth_client
    Transaction.objects.create(user=user, date='2025-08-01', amount=100, currency='TRY', type='credit', description='Satış', category='Gelir', unique_hash='hash1')
    Transaction.objects.create(user=user, date='2025-08-02', amount=50, currency='TRY', type='debit', description='Kira', category='Kira Gideri', unique_hash='hash2')

    url = reverse('reports-summary')
    response = client.get(url, {'start_date':'2025-08-01', 'end_date':'2025-08-31'})
    assert response.status_code == 200
    assert response.data['total_income'] == '100.00'
    assert response.data['total_expense'] == '50.00'
    assert response.data['net_cash_flow'] == '50.00'
