import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from configapp.models import Payout


@pytest.mark.django_db
def test_create_payout_success():
    client = APIClient()
    data = {
        "amount": "100.50",
        "currency": "usd",
        "recipient": "John Doe, Account 123",
        "description": "Test payout"
    }
    resp = client.post('/api/payouts/', data, format='json')
    assert resp.status_code == 201
    body = resp.json()
    assert body['amount'] == '100.50'
    assert body['currency'] == 'USD'
    assert Payout.objects.filter(id=body['id']).exists()
