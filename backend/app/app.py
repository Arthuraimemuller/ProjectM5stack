from flask import Flask, request, jsonify
import os
import hashlib
from api.bigquery_service import BigQueryService
from dotenv import load_dotenv
import datetime
import socket
app = Flask(__name__)
load_dotenv("config/secrets.env")

EXPECTED_PASSWD_HASH = os.getenv("EXPECTED_PASSWD_HASH")

bq_service = BigQueryService()

def verify_password_hash(received_hash: str) -> bool:
    return received_hash == EXPECTED_PASSWD_HASH

@app.route('/send-to-bigquery', methods=['POST'])
def receive_data():
    data = request.get_json(force=True)
    if not data or "passwd" not in data or "values" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    if not verify_password_hash(data["passwd"]):
        return jsonify({"error": "Unauthorized"}), 401

    values = data["values"]
    date = values.get("date")
    time = values.get("time")
    indoor_temp = values.get("indoor_temp")
    indoor_humidity = values.get("indoor_humidity")

    if None in (date, time, indoor_temp, indoor_humidity):
        return jsonify({"error": "Missing sensor data"}), 400

    try:
        bq_service.insert_sensor_data(date, time, indoor_temp, indoor_humidity)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':



    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("Mon IP locale est :", local_ip)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))