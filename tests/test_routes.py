import pytest

pytestmark = pytest.mark.asyncio

async def test_score_transaction_returns_201(client):
    payload = {
        "amount": "150.00", "currency": "gbp", "merchant_category_code": "5411",
        "channel": "contactless", "country_code": "gb", "card_holder_country": "gb",
        "hour_of_day": 14, "is_international": False,
    }
    response = await client.post("/transactions", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "allow"

async def test_score_transaction_invalid_channel_returns_400(client):
    payload = {
        "amount": "10.00", "currency": "GBP", "merchant_category_code": "5411",
        "channel": "carrier_pigeon", "country_code": "GB", "card_holder_country": "GB",
        "hour_of_day": 10, "is_international": False,
    }
    response = await client.post("/transactions", json=payload)
    assert response.status_code == 400

async def test_score_transaction_negative_amount_returns_422(client):
    payload = {
        "amount": "-5.00", "currency": "GBP", "merchant_category_code": "5411",
        "channel": "online", "country_code": "GB", "card_holder_country": "GB",
        "hour_of_day": 10, "is_international": False,
    }
    response = await client.post("/transactions", json=payload)
    assert response.status_code == 422

async def test_get_transaction_round_trip(client):
    create_payload = {
        "amount": "3500.00", "currency": "GBP", "merchant_category_code": "5411",
        "channel": "online", "country_code": "RO", "card_holder_country": "GB",
        "hour_of_day": 3, "is_international": True,
    }
    create_response = await client.post("/transactions", json=create_payload)
    txn_id = create_response.json()["transaction_id"]

    get_response = await client.get(f"/transactions/{txn_id}")
    assert get_response.status_code == 200
    assert get_response.json()["decision"] == "block"

async def test_get_nonexistent_transaction_returns_404(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/transactions/{fake_id}")
    assert response.status_code == 404

async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
