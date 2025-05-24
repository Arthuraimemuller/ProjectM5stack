from flask import Blueprint, jsonify, request
from app.services.openweather_service import OpenWeatherService

weather_api = Blueprint('weather_api', __name__)

# Instance globale (avec settings par défaut)
weather_service = OpenWeatherService()

@weather_api.route('/api/v1/weather/current', methods=['GET'])
def current_weather():
    try:
        data = weather_service.get_current_weather()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Si tu veux l'appeler dynamiquement (via query params)
@weather_api.route('/api/v1/weather/city', methods=['GET'])
def weather_by_city():
    city = request.args.get('city', 'Geneva')
    country = request.args.get('country', 'CH')
    try:
        service = OpenWeatherService(city=city, country_code=country)
        data = service.get_current_weather()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
