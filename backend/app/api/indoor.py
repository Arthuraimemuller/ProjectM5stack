from flask import Blueprint, jsonify, current_app
from ..services.bigquery_service import BigQueryService
from flask import request
from typing import Optional

# Define blueprint
indoor_api = Blueprint("indoor_api", __name__, url_prefix="/api/v1/indoor")

# ✅ Pro — retarde l'instanciation
bq_service: Optional[BigQueryService] = None

def init_indoor_routes():
    global bq_service
    bq_service = BigQueryService()


@indoor_api.route("/measurements", methods=["GET"])
def get_indoor_measurements():
    """
    Returns the latest indoor measurements (temperature, humidity, etc.)
    retrieved from BigQuery.
    """
    try:
        data = bq_service.get_latest_indoor_data()
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"[IndoorAPI] Failed to fetch data: {e}")
        return jsonify({"error": "Failed to fetch indoor data"}), 500



@indoor_api.route("/history", methods=["GET"])
def get_indoor_history():
    """
    Returns the last N indoor measurements from BigQuery.
    ?limit=10
    """
    try:
        limit = int(request.args.get("limit", 10))
        data = bq_service.get_last_n_indoor_measurements(limit)
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"[IndoorAPI] Failed to fetch history: {e}")
        return jsonify({"error": "Failed to fetch indoor history"}), 500

