import requests

BASE_URL = "http://localhost:8080"  # Change le port si besoin !

def test_current_weather():
    url = f"{BASE_URL}/api/v1/weather/current"
    response = requests.get(url)
    print("\n== GET /api/v1/weather/current ==")
    print("Status:", response.status_code)
    print("Response:", response.json())

def test_weather_by_city(city="Paris", country="FR"):
    url = f"{BASE_URL}/api/v1/weather/city"
    params = {"city": city, "country": country}
    response = requests.get(url, params=params)
    print(f"\n== GET /api/v1/weather/city?city={city}&country={country} ==")
    print("Status:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_current_weather()
    test_weather_by_city("Geneva", "CH")
    test_weather_by_city("Paris", "FR")

