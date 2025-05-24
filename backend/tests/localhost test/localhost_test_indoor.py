import requests
import json

# === CONFIG ===
BASE_URL = "http://localhost:8080"  # ou le port que tu utilises


# === TEST ENDPOINT: Dernière mesure indoor ===
def test_latest_indoor_measurement():
    url = f"{BASE_URL}/api/v1/indoor/measurements"
    print(f"🔍 Test GET {url}")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ Réponse reçue :")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        print(response.text)


# === TEST ENDPOINT: Historique limité ===
def test_indoor_history(limit=3):
    url = f"{BASE_URL}/api/v1/indoor/history?limit={limit}"
    print(f"\n🔍 Test GET {url}")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ Historique reçu :")
        for entry in data:
            print(json.dumps(entry, indent=2))
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        print(response.text)


# === Lancer les tests ===
if __name__ == "__main__":
    test_latest_indoor_measurement()
    test_indoor_history(limit=5)
