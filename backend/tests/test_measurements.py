import unittest
from app import create_app
from config import load_config

class MeasurementsApiTestCase(unittest.TestCase):
    def setUp(self):
        load_config()  # Assure que les .env sont chargés
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_latest_measurements(self):
        """Test du endpoint GET /api/v1/measurements/latest"""
        response = self.client.get("/api/v1/measurements/latest")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("timestamp", data)

    def test_measurements_history(self):
        """Test du endpoint GET /api/v1/measurements/history?limit=3"""
        response = self.client.get("/api/v1/measurements/history?limit=3")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertLessEqual(len(data), 3)
        if data:
            self.assertIn("timestamp", data[0])

if __name__ == "__main__":
    unittest.main()