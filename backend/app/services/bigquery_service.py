from google.cloud import bigquery
import os
from datetime import datetime
from typing import Optional


class BigQueryService:
    """
    Service to interact with Google BigQuery for inserting sensor data.
    """

    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = os.getenv("BQ_DATASET_ID")
        self.table_id = os.getenv("BQ_TABLE_ID")

        if not all([self.project_id, self.dataset_id, self.table_id]):
            raise ValueError("Missing one or more BigQuery environment variables.")

        self.client = bigquery.Client(project=self.project_id)
        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    def insert_sensor_data(
            self,
            indoor_temp: float,
            indoor_humidity: float,
            air_quality: Optional[float] = None,
            co2: Optional[int] = None,
            tvoc: Optional[int] = None,
            timestamp: Optional[str] = None
    ) -> bool:
        """
        Insert a row of indoor sensor data into BigQuery.

        :param indoor_temp: Temperature in °C
        :param indoor_humidity: Humidity in %
        :param air_quality: Optional air quality index
        :param co2: Optional CO2 level in ppm
        :param tvoc: Optional TVOC value
        :param timestamp: Optional ISO timestamp (if None, use now)
        :return: True if successful, else raise
        """
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()

        row = {
            "timestamp": timestamp,
            "indoor_temp": indoor_temp,
            "indoor_humidity": indoor_humidity,
        }

        # Add optional values if provided
        if air_quality is not None:
            row["air_quality"] = air_quality
        if co2 is not None:
            row["co2"] = co2
        if tvoc is not None:
            row["tvoc"] = tvoc

        errors = self.client.insert_rows_json(self.full_table_id, [row])
        if errors:
            raise RuntimeError(f"Failed to insert rows: {errors}")
        return True

    def get_latest_indoor_data(self) -> dict:
        """
        Retrieves the most recent indoor measurement from BigQuery.

        :return: dict with keys like temperature, humidity, etc.
        """
        query = f"""
            SELECT *
            FROM `{self.full_table_id}`
            ORDER BY timestamp DESC
            LIMIT 1
        """

        try:
            query_job = self.client.query(query)
            result = query_job.result()
            row = next(iter(result), None)

            if row:
                return {
                    "timestamp": row.get("timestamp"),
                    "indoor_temp": row.get("indoor_temp"),
                    "indoor_humidity": row.get("indoor_humidity"),
                    "air_quality": row.get("air_quality", None),
                    "co2": row.get("co2", None),
                    "tvoc": row.get("tvoc", None),
                }

            return {"error": "No data found in BigQuery."}

        except Exception as e:
            raise RuntimeError(f"Failed to fetch indoor data: {e}")


    def get_last_n_indoor_measurements(self, limit: int = 10) -> list:
        """
        Retrieve the last N indoor measurements from BigQuery.

        :param limit: Number of rows to retrieve
        :return: List of dicts
        """
        query = f"""
            SELECT *
            FROM `{self.full_table_id}`
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        try:
            query_job = self.client.query(query)
            results = query_job.result()

            rows = []
            for row in results:
                rows.append({
                    "timestamp": row.get("timestamp"),
                    "indoor_temp": row.get("indoor_temp"),
                    "indoor_humidity": row.get("indoor_humidity"),
                    "air_quality": row.get("air_quality", None),
                    "co2": row.get("co2", None),
                    "tvoc": row.get("tvoc", None),
                })

            return rows

        except Exception as e:
            raise RuntimeError(f"Failed to fetch history from BigQuery: {e}")
