from flask import Blueprint, jsonify, current_app
from ..services.openweather_service import OpenWeatherService
import os

outdoor_api = Blueprint("outdoor_api", __name__)

# Initialisation du service avec variables d'environnement
weather_service = OpenWeatherService(
    api_key=os.getenv("OPENWEATHER_API_KEY"),
    city=os.getenv("CITY", "Geneva"),
    country_code=os.getenv("COUNTRY_CODE", "CH")
)

@outdoor_api.route("/api/v1/outdoor/current", methods=["GET"])
def get_current_outdoor_weather():
    """
    Returns current outdoor weather: temperature and humidity.
    """
    try:
        data = weather_service.get_current_weather()
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"Error fetching current weather: {e}")
        return jsonify({"error": "Failed to fetch current weather"}), 500

@outdoor_api.route("/api/v1/outdoor/forecast", methods=["GET"])
def get_outdoor_forecast():
    """
    Returns 7-day forecast for outdoor temperature and weather icon.
    """
    try:
        forecast = weather_service.get_forecast()
        return jsonify(forecast)
    except Exception as e:
        current_app.logger.error(f"Error fetching forecast: {e}")
        return jsonify({"error": "Failed to fetch forecast"}), 500
