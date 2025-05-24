import unittest
from app import create_app

class WeatherApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_current_weather(self):
        """Test GET /api/v1/weather/current returns expected keys."""
        response = self.client.get('/api/v1/weather/current')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIsInstance(data['temperature'], (int, float))
        self.assertIsInstance(data['humidity'], (int, float))

    def test_weather_by_city(self):
        """Test GET /api/v1/weather/city?city=Paris&country=FR."""
        response = self.client.get('/api/v1/weather/city?city=Paris&country=FR')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)

if __name__ == "__main__":
    unittest.main()
