import requests
import time
from datetime import datetime

API_KEY = "72dbcc9258a8493ae64994a80e22e830"
CITY = "Geneva"
COUNTRY = "CH"

def get_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY},{COUNTRY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    daily_forecast = {}

    # Parcours des prévisions toutes les 3h
    for item in data['list']:
        dt_txt = item['dt_txt']  # ex: '2025-05-22 12:00:00'
        date_str, time_str = dt_txt.split(' ')
        hour = int(time_str.split(':')[0])
        diff = abs(hour - 12)  # distance à midi

        # Si pas encore de donnée pour ce jour, ou si celle-ci est plus proche de midi, on met à jour
        if date_str not in daily_forecast or diff < daily_forecast[date_str]['diff']:
            daily_forecast[date_str] = {
                'temp': round(item['main']['temp'], 1),
                'diff': diff
            }

    # Affichage des résultats
    for date, info in sorted(daily_forecast.items()):
        print(f"{date} : {info['temp']}°C (diff {info['diff']}h)")

if __name__ == "__main__":
    get_forecast()
