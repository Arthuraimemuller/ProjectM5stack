import requests
import json

BASE_URL = "http://localhost:8080"  # ou 5000 selon ton app

def test_latest_measurement():
    url = f"{BASE_URL}/api/v1/measurements/latest"
    print(f"🔍 GET {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("✅ Dernière mesure :")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"❌ Erreur : {e}")

def test_measurement_history(limit=3):
    url = f"{BASE_URL}/api/v1/measurements/history?limit={limit}"
    print(f"\n🔍 GET {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ {len(data)} mesures récentes :")
        for row in data:
            print(json.dumps(row, indent=2))
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    test_latest_measurement()
    test_measurement_history(3)
