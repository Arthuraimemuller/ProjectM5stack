import hashlib
import requests
import datetime

def test_send_to_bigquery_success():
    raw_password = "ThisIsAStrongPassword"
    hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()
    now = datetime.datetime.now()
    print("now =", now)
    print("date =", now.strftime("%Y-%m-%d"))
    print("time =", now.strftime("%H:%M:%S"))
    data = {
        "passwd": "943912667b08be19402bfc3a51a921cfc85f794938d4e23a1b7e37013c453f1e",
        "values": {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "indoor_temp": 23,
            "indoor_humidity": 58
        }
    }

    url = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/send-to-bigquery"
    response = requests.post(url, json=data)

    assert response.status_code == 200, f"Error {response.status_code}: {response.text}"
    assert "success" in response.text.lower()

if __name__ == "__main__":
    test_send_to_bigquery_success()
