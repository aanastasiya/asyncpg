import time

import unittest
from unittest.mock import patch, MagicMock, create_autospec
from fastapi.testclient import TestClient
from asyncpg.exceptions import PostgresError

from main import app, query_source
from models import Data1


class TestApp(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('main.query_source')
    def test_get_data_success(self, mock_query):
        mock = create_autospec(query_source, return_value=[Data1(id=1, name='Test 1')])
        mock_query.return_value = mock.return_value

        response = self.client.get('/data/')
        self.assertEqual(response.status_code, 200)

        expected_data = [
            {'id': 1, 'name': 'Test 1'},
            {'id': 1, 'name': 'Test 1'},
            {'id': 1, 'name': 'Test 1'}
        ]
        self.assertEqual(response.json(), expected_data)

    @patch('main.query_source')
    def test_get_data_error(self, mock_query):
        mock = MagicMock()
        mock.side_effect = PostgresError('Mock error')
        mock_query.return_value = mock

        response = self.client.get('/data/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), [])

    @patch('main.query_source')
    def test_get_data_timeout(self, mock_query):
        mock = create_autospec(query_source, return_value=[Data1(id=1, name='Test 1')])
        mock.side_effect = time.sleep(3)
        mock_query = mock

        response = self.client.get('/data/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), [])


if __name__ == '__main__':
    unittest.main()
