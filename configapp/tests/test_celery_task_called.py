import pytest
from unittest import mock
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_task_called_on_create(monkeypatch):
    client = APIClient()
    data = {
        "amount": "10.00",
        "currency": "EUR",
        "recipient": "A",
    }

    from payouts import tasks
    called = {}
    def fake_delay(payout_id):
        called['id'] = payout_id
    monkeypatch.setattr(tasks.process_payout_task, 'delay', fake_delay)

    resp = client.post('/api/payouts/', data, format='json')
    assert resp.status_code == 201
    assert 'id' in called
