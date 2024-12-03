import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_analyze_route(self):
        response = self.client.post("/analyze", json={"text": "Hello world!"})
        self.assertEqual(response.status_code, 200)