import requests

BASE_URL = "http://localhost:8080"  # adapte si tu utilises un autre port !

def test_forecast_default():
    url = f"{BASE_URL}/api/v1/forecast"
    response = requests.get(url)
    print("\n== GET /api/v1/forecast (default hour) ==")
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Raw content:", response.text)

def test_forecast_with_hour(hour):
    url = f"{BASE_URL}/api/v1/forecast"
    params = {"hour": hour}
    response = requests.get(url, params=params)
    print(f"\n== GET /api/v1/forecast?hour={hour} ==")
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Raw content:", response.text)

if __name__ == "__main__":
    test_forecast_default()
    test_forecast_with_hour(8)
    test_forecast_with_hour(18)
