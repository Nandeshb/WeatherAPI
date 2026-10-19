import requests
from app import app

def test_health_check():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Weather API is running"


def test_missing_city():
    client = app.test_client()

    response = client.get("/weather")

    assert response.status_code == 400
    assert "error" in response.json


from unittest.mock import Mock, patch


@patch("app.requests.get")
def test_unknown_city(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = app.test_client()
    response = client.get("/weather?city=xyzqwerty987")

    assert response.status_code == 404
    assert "not found" in response.json["error"].lower()


@patch("app.requests.get")
def test_weather_success(mock_get):
    # Mock the geocoding API response
    location_response = Mock()
    location_response.json.return_value = {
        "results": [
            {
                "name": "Bengaluru",
                "country": "India",
                "latitude": 12.97,
                "longitude": 77.59,
            }
        ]
    }
    location_response.raise_for_status.return_value = None

    # Mock the weather API response
    weather_response = Mock()
    weather_response.json.return_value = {
        "current": {
            "temperature_2m": 25.0,
            "apparent_temperature": 26.0,
            "relative_humidity_2m": 60,
            "weather_code": 1,
            "wind_speed_10m": 8.0,
            "time": "2026-10-18T10:00",
        }
    }
    weather_response.raise_for_status.return_value = None

    # Return the two mocked responses in order
    mock_get.side_effect = [
        location_response,
        weather_response
    ]

    client = app.test_client()
    response = client.get("/weather?city=Bengaluru")

    # Verify the API response
    assert response.status_code == 200
    assert response.json["city"] == "Bengaluru"
    assert response.json["country"] == "India"
    assert response.json["temperature_c"] == 25.0
    assert response.json["condition"] == "Mainly clear"
    assert mock_get.call_count == 2


@patch("app.requests.get")
def test_weather_service_failure(mock_get):
    # The geocoding service responds successfully
    location_response = Mock()
    location_response.json.return_value = {
        "results": [
            {
                "name": "Bengaluru",
                "country": "India",
                "latitude": 12.97,
                "longitude": 77.59,
            }
        ]
    }
    location_response.raise_for_status.return_value = None

    # The weather service fails on the second request
    mock_get.side_effect = [
        location_response,
        requests.RequestException("Service unavailable"),
    ]

    client = app.test_client()
    response = client.get("/weather?city=Bengaluru")

    assert response.status_code == 502
    assert "error" in response.json

