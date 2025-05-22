import requests

BASE_URL = "https://docker-flask-backend-project-688745668065.europe-west6.run.app"

def test_current_weather():
    url = f"{BASE_URL}/weather/current"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Current Weather:", data)
        assert "temperature" in data and "humidity" in data
        print("Test current_weather passed!")
    else:
        print("Failed to get current weather:", response.status_code, response.text)

def test_weather_forecast():
    url = f"{BASE_URL}/weather/forecast"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Weather Forecast:")
        for day in data:
            print(day)
        assert isinstance(data, list) and len(data) > 0
        print("Test weather_forecast passed!")
    else:
        print("Failed to get weather forecast:", response.status_code, response.text)

if __name__ == "__main__":
    test_current_weather()
    test_weather_forecast()
