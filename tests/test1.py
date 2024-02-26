import unittest
from app import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Flask Web Application!", response.data)

    def test_api_data_get(self):
        response = self.app.get('/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Send a POST request with data", response.data)

    def test_api_data_post(self):
        response = self.app.post('/api/data', json={"key": "value"})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"received_data", response.data)

if __name__ == '_main_':
   unittest.main()