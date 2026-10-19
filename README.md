
# Weather API

A beginner-friendly REST API built with Python and Flask that retrieves current weather information for a city using Open-Meteo.

## Features

- Retrieve current weather by city name
- Get temperature, feels-like temperature, humidity, and wind speed
- Convert weather codes into readable descriptions
- Validate missing and unknown city names
- Handle external API request failures
- Test endpoints using Postman
- Run automated backend tests using pytest
- Measure code coverage using pytest-cov

## Tech Stack

- Python
- Flask
- Requests
- Open-Meteo Geocoding API
- Open-Meteo Weather API
- Postman
- pytest
- pytest-cov

## Project Structure

```text
WeatherAPI/
├── app.py
├── test_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.venv/` directory contains the local Python environment and is excluded from Git.

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd WeatherAPI
```

Replace the placeholder URL with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The server starts at:

http://127.0.0.1:5000

If your virtual environment uses a different Python executable path, use that environment's Python executable to run these commands.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/weather?city=Bengaluru` | Retrieve weather for a city |

### Example request

```http
GET /weather?city=Bengaluru
```

### Example response

```json
{
  "city": "Bengaluru",
  "country": "India",
  "temperature_c": 25.0,
  "feels_like_c": 26.0,
  "humidity_percent": 60,
  "condition": "Mainly clear",
  "wind_speed_kmh": 8.0,
  "time": "2026-10-18T10:00"
}
```

The values above are illustrative, not live weather readings.

## HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 400 | City parameter is missing |
| 404 | City was not found |
| 502 | External weather service request failed |

## Automated Testing

Run the full test suite:

```bash
python -m pytest -v
```

Run the tests with code coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing -v
```

The tests cover health checks, input validation, unknown cities, successful weather responses, and external service failures.

External API responses are mocked during unit tests to make them predictable.

## External APIs

- Open-Meteo Geocoding API: https://open-meteo.com/en/docs/geocoding-api
- Open-Meteo Weather API: https://open-meteo.com/en/docs

This project uses Open-Meteo for learning and development. Review its terms for your intended usage.

## Learning Objectives

This project demonstrates practical skills in:

- Python backend development
- REST API design
- HTTP requests and JSON responses
- Input validation and error handling
- API testing with Postman
- Automated testing with pytest
- Code coverage analysis
