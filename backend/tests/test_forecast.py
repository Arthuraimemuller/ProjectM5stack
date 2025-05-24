import unittest
from app import create_app

class ForecastApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_forecast(self):
        """Test GET /api/v1/forecast returns a list of forecasts."""
        response = self.client.get('/api/v1/forecast')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertLessEqual(len(data), 7)
        if data:
            self.assertIn('date', data[0])
            self.assertIn('temp', data[0])
            self.assertIn('icon', data[0])

    def test_forecast_with_hour(self):
        """Test GET /api/v1/forecast?hour=18."""
        response = self.client.get('/api/v1/forecast?hour=18')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
