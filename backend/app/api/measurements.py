from flask import Blueprint, jsonify, current_app, request
from ..services.bigquery_service import BigQueryService
from typing import Optional
import traceback

measurements_api = Blueprint("measurements_api", __name__, url_prefix="/api/v1/measurements")

bq_service: Optional[BigQueryService] = None

def init_measurements_routes():
    global bq_service
    bq_service = BigQueryService()

@measurements_api.route("/latest", methods=["GET"])
def get_latest_measurement():
    """
    Returns the most recent full measurement entry (indoor + outdoor).
    """
    try:
        data = bq_service.get_latest_measurement()
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"[MeasurementsAPI] Failed to fetch latest measurement: {e}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "Failed to fetch latest measurement"}), 500

@measurements_api.route("/history", methods=["GET"])
def get_measurement_history():
    """
    Returns the last N measurements. Default limit is 10.
    Example: GET /api/v1/measurements/history?limit=5
    """
    try:
        limit = max(1, int(request.args.get("limit", 10)))
        data = bq_service.get_last_n_measurements(limit)
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"[MeasurementsAPI] Failed to fetch measurement history: {e}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "Failed to fetch measurement history"}), 500
