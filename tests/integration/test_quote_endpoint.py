import os

from fastapi.testclient import TestClient

from app.main import create_app


def test_should_return_quote_simulation() -> None:
    os.environ["CURRENT_YEAR"] = "2022"
    client = TestClient(create_app())
    response = client.post(
        "/quotes/simulate",
        json={
            "car": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2012,
                "value": 100000.0,
            },
            "deductible_percentage": 0.1,
            "broker_fee": 50.0,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["car"]["make"] == "Toyota"
    assert payload["car"]["model"] == "Corolla"
    assert payload["car"]["year"] == 2012
    assert payload["car"]["value"] == 100000.0
    assert payload["applied_rate"] == 0.1
    assert payload["deductible_value"] == 10000.0
    assert payload["policy_limit"] == 90000.0
    assert payload["calculated_premium"] == 9050.0


def test_should_validate_invalid_payload() -> None:
    os.environ["CURRENT_YEAR"] = "2022"
    client = TestClient(create_app())
    response = client.post(
        "/quotes/simulate",
        json={
            "car": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 1800,
                "value": 100000.0,
            },
            "deductible_percentage": 1.5,
            "broker_fee": -1,
        },
    )
    assert response.status_code == 422
