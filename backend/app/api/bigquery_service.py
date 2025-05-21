from google.cloud import bigquery
import os

class BigQueryService:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = os.getenv("BQ_DATASET_ID")
        self.table_id = os.getenv("BQ_TABLE_ID")  # just table name
        self.client = bigquery.Client(project=self.project_id)
        # Full table identifier: project.dataset.table
        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    def insert_sensor_data(self, date, time, indoor_temp, indoor_humidity):
        rows_to_insert = [
            {
                "date": date,
                "time": time,
                "indoor_temp": indoor_temp,
                "indoor_humidity": indoor_humidity
            }
        ]

        errors = self.client.insert_rows_json(self.full_table_id, rows_to_insert)
        if errors:
            raise RuntimeError(f"Failed to insert rows: {errors}")
        return True
