
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


def describe_weather(code):
    """Convert a weather code into a readable description."""
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return descriptions.get(code, "Other weather conditions")


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Weather API is running"
    })


@app.route("/weather", methods=["GET"])
def get_weather():
    # Read the city name from the URL
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({
            "error": "Please provide a city name."
        }), 400

    try:
        # Step 1: Find the city's coordinates
        location_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        location_response.raise_for_status()

        locations = location_response.json().get("results", [])

        if not locations:
            return jsonify({
                "error": f"City '{city}' was not found."
            }), 404

        location = locations[0]

        # Step 2: Fetch weather for those coordinates
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        # Step 3: Return a clean JSON response
        return jsonify({
            "city": location["name"],
            "country": location.get("country"),
            "temperature_c": current["temperature_2m"],
            "feels_like_c": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "condition": describe_weather(current["weather_code"]),
            "wind_speed_kmh": current["wind_speed_10m"],
            "time": current["time"]
        })

    except requests.RequestException:
        return jsonify({
            "error": "Unable to reach the weather service. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
