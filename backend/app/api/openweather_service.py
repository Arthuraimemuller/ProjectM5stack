import requests
import os

class OpenWeatherService:
    """
    Service to interact with OpenWeather API for current weather and forecast data.
    """

    BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
    BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key: str, city: str, country_code: str):
        """
        :param api_key: OpenWeather API key
        :param city: City name (e.g., "Geneva")
        :param country_code: Country code (e.g., "CH")
        """
        self.api_key = api_key
        self.city = city
        self.country_code = country_code

    def get_current_weather(self):
        """
        Fetch current weather data: temperature and humidity.
        :return: dict with keys 'temperature' (°C) and 'humidity' (%)
        """
        params = {
            "q": f"{self.city},{self.country_code}",
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.BASE_URL_CURRENT, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"]
        }

    def get_forecast(self, target_hour=12):
        """
        Fetch 7-day forecast data at a given hour (default noon).
        :param target_hour: Hour of the day to pick forecast for each day (0-23)
        :return: List of dicts, each with keys: 'date', 'temp', 'icon'
        """
        params = {
            "q": f"{self.city},{self.country_code}",
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.BASE_URL_FORECAST, params=params)
        response.raise_for_status()
        data = response.json()

        # Organize forecast by date: pick entry closest to target_hour
        daily_forecast = {}
        for item in data['list']:
            dt_txt = item['dt_txt']  # format 'YYYY-MM-DD HH:MM:SS'
            date_str, time_str = dt_txt.split(' ')
            hour = int(time_str.split(':')[0])

            diff = abs(hour - target_hour)
            if date_str not in daily_forecast or diff < daily_forecast[date_str]['diff']:
                daily_forecast[date_str] = {
                    "temp": item['main']['temp'],
                    "icon": item['weather'][0]['icon'],
                    "diff": diff
                }

        # Extract next 7 days sorted
        sorted_dates = sorted(daily_forecast.keys())
        forecast_list = []
        for date in sorted_dates[:7]:
            forecast_list.append({
                "date": date,
                "temp": round(daily_forecast[date]['temp'], 1),
                "icon": daily_forecast[date]['icon']
            })

        return forecast_list
