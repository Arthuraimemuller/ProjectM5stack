from google.cloud import bigquery
from datetime import datetime
from typing import Optional
from config import settings  # Import depuis ton module de config


class BigQueryService:
    """
    Service to interact with Google BigQuery for inserting sensor and weather data.
    """

    def __init__(self):
        self.project_id = settings.GCP_PROJECT_ID
        self.dataset_id = settings.BQ_DATASET_ID
        self.table_id = settings.BQ_TABLE_ID

        if not all([self.project_id, self.dataset_id, self.table_id]):
            raise ValueError("Missing one or more BigQuery environment variables.")

        self.client = bigquery.Client(project=self.project_id)
        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    def insert_sensor_data(
        self,
        device_id: str,
        timestamp: Optional[str] = None,
        indoor_temp: Optional[float] = None,
        indoor_humidity: Optional[float] = None,
        indoor_co2: Optional[int] = None,
        indoor_tvoc: Optional[int] = None,
        motion_detected: Optional[bool] = None,
        outdoor_temp: Optional[float] = None,
        outdoor_humidity: Optional[float] = None,
        outdoor_pressure: Optional[float] = None,
        outdoor_wind_speed: Optional[float] = None,
        outdoor_weather: Optional[str] = None,
        source: Optional[str] = "M5Stack+OpenWeather"
    ) -> bool:
        """
        Insert a full indoor/outdoor data row into BigQuery.
        """
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()

        row = {
            "timestamp": timestamp,
            "device_id": device_id,
            "indoor_temp": indoor_temp,
            "indoor_humidity": indoor_humidity,
            "indoor_co2": indoor_co2,
            "indoor_tvoc": indoor_tvoc,
            "motion_detected": motion_detected,
            "outdoor_temp": outdoor_temp,
            "outdoor_humidity": outdoor_humidity,
            "outdoor_pressure": outdoor_pressure,
            "outdoor_wind_speed": outdoor_wind_speed,
            "outdoor_weather": outdoor_weather,
            "source": source
        }

        # Supprimer les clés avec valeur None (facultatif, pour éviter les NULL explicites)
        clean_row = {k: v for k, v in row.items() if v is not None}

        errors = self.client.insert_rows_json(self.full_table_id, [clean_row])
        if errors:
            raise RuntimeError(f"Failed to insert rows: {errors}")
        return True

    def get_latest_measurement(self) -> dict:
        """
        Retrieves the most recent full measurement (indoor + outdoor).
        """
        query = f"""
            SELECT *
            FROM `{self.full_table_id}`
            ORDER BY timestamp DESC
            LIMIT 1
        """

        try:
            query_job = self.client.query(query)
            row = next(iter(query_job.result()), None)

            if row:
                return dict(row)
            else:
                return {"error": "No data found in BigQuery."}

        except Exception as e:
            raise RuntimeError(f"Failed to fetch latest data: {e}")

    def get_last_n_measurements(self, limit: int = 10) -> list:
        """
        Retrieve the last N measurements from BigQuery.
        """
        query = f"""
            SELECT *
            FROM `{self.full_table_id}`
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        try:
            query_job = self.client.query(query)
            return [dict(row) for row in query_job.result()]

        except Exception as e:
            raise RuntimeError(f"Failed to fetch last {limit} rows: {e}")
