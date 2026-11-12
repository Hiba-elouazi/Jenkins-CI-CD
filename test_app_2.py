import unittest
from app import app


class TestAppEdgeCases(unittest.TestCase):
    """Deuxième fichier de tests : cas limites, lancé en parallèle de test_app.py."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_sum_negative_numbers(self):
        response = self.client.post('/sum', data={'a': '-4', 'b': '-6'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'-10.0', response.data)

    def test_sum_decimal_numbers(self):
        response = self.client.post('/sum', data={'a': '2.5', 'b': '0.25'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2.75', response.data)

    def test_sum_missing_values_default_to_zero(self):
        response = self.client.post('/sum', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result: 0.0', response.data)

    def test_hello_strips_spaces(self):
        response = self.client.post('/hello', data={'username': '   Hiba   '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Hiba, welcome', response.data)

    def test_hello_only_spaces_is_anonymous(self):
        response = self.client.post('/hello', data={'username': '    '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello there', response.data)

    def test_sum_rejects_get(self):
        response = self.client.get('/sum')
        self.assertEqual(response.status_code, 405)

    def test_unknown_route_returns_404(self):
        response = self.client.get('/does-not-exist')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
