from flask import Blueprint, jsonify, request
from app.services.openweather_service import OpenWeatherService

forecast_api = Blueprint('forecast_api', __name__)

weather_service = OpenWeatherService()

@forecast_api.route('/api/v1/forecast', methods=['GET'])
def get_forecast():
    target_hour = int(request.args.get('hour', 12))
    try:
        data = weather_service.get_forecast(target_hour=target_hour)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
