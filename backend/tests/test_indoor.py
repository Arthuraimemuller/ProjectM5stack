import unittest
from app import create_app

class IndoorApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_latest_measurements(self):
        """Test du endpoint GET /api/v1/indoor/measurements"""
        response = self.client.get("/api/v1/indoor/measurements")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("indoor_temp", data)
        self.assertIn("indoor_humidity", data)

    def test_indoor_history(self):
        """Test du endpoint GET /api/v1/indoor/history?limit=3"""
        response = self.client.get("/api/v1/indoor/history?limit=3")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertLessEqual(len(data), 3)
        if data:
            self.assertIn("timestamp", data[0])
            self.assertIn("indoor_temp", data[0])

if __name__ == "__main__":
    unittest.main()
