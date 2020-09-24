import unittest
from unittest.mock import patch
from server import connex_app # pylint: disable=F0401
from get_finance_data import symbols # pylint: disable=F0401
from models.ohlc import OHLC # pylint: disable=F0401
from tests.mock_database_response import mock_db_query # pylint: disable=F0401

mock_db_response = mock_db_query()

class TestAPIOperations(unittest.TestCase):
    def setUp(self):
        self.client = connex_app.app.test_client()

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_response_is_always_json(self, queryMOCK):
        """
        GIVEN any url
        WHEN a request is made
        THEN should return a JSON response
        """
        # Setup database mock query        
        queryMOCK.return_value.filter.return_value.all.return_value = mock_db_response

        rv = self.client.get("/")
        self.assertTrue(rv.is_json)
        rv = self.client.get("/api/v1/AAPL")
        self.assertTrue(rv.is_json)
        rv = self.client.get("/api/v1/ohlc/AAPL?start_time=2020-09-24%2010%3A37%3A09.000000&end_time=2020-09-24%2010%3A37%3A09.000000")
        self.assertTrue(rv.is_json)

    def test_route_not_found_error_code(self):
        """
        GIVEN a wrong url
        WHEN a request is made
        THEN should return a 404 error code
        """
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 404)
        self.assertTrue(rv.is_json)

    def test_url_not_found_error_message(self):
        """
        GIVEN a wrong url
        WHEN a request is made
        THEN should return an appropriate error message
        """
        rv = self.client.get("/")
        self.assertTrue(rv.is_json)
        body = rv.get_json()
        self.assertEqual(body["status"], 404)
        self.assertEqual(body["detail"], "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

    def test_symbol_must_be_supported_symbol(self):
        """
        GIVEN a url with an unsupported symbol paramater
        WHEN a request is made
        THEN should return bad request error including a list of supported symbols
        """
        rv = self.client.get("/api/v1/ohlc/***?start_time=2020-09-24%2010%3A37%3A09.000000&end_time=2020-09-24%2010%3A37%3A09.000000")
        self.assertTrue(rv.is_json)
        self.assertEqual(rv.status_code, 400)
        body = rv.get_json()
        self.assertEqual(body["success"], False)
        self.assertEqual(body["message"], "Invalid symbol provided: ***. Supported symbols are " + ",".join(symbols))

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_api_empty_data_response(self, queryMOCK):
        """
        GIVEN a valid query url with the correct supported parameters
        WHEN a request is made and no data is found for the symbol
        THEN should return 404 not found response
        """
        # Setup database mock query        
        queryMOCK.return_value.filter.return_value.all.return_value = []

        rv = self.client.get("/api/v1/ohlc/AAPL?start_time=2020-09-24%2010%3A37%3A09.000000&end_time=2020-09-24%2010%3A37%3A09.000000") # mock empty data endpoint
        self.assertTrue(rv.is_json)
        self.assertEqual(rv.status_code, 404)
        body = rv.get_json()
        self.assertEqual(body["success"], False)
        self.assertEqual(body["message"], "No data found for symbol: AAPL in time frame 2020-09-24 10:37:09.000000 to 2020-09-24 10:37:09.000000")
    
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_api_success_response_for_valid_query(self, queryMOCK):
        """
        GIVEN a valid query url with the correct supported parameters
        WHEN a request is made
        THEN should return 200 with all the required information
        """
        # Setup database mock query        
        queryMOCK.return_value.filter.return_value.all.return_value = mock_db_response

        rv = self.client.get("/api/v1/ohlc/AAPL?start_time=2020-09-24%2010%3A37%3A09.000000&end_time=2020-09-24%2010%3A37%3A09.000000")
        self.assertTrue(rv.is_json)
        self.assertEqual(rv.status_code, 200)
        body = rv.get_json()
        self.assertEqual(body["success"], True)
        self.assertEqual(body["message"], "OHLC data obtained successfully")
        expected_response = [{'created_at': '2020-09-24T14:37:44.181335', 'data_id': 1133, 's_close': 107.91999816894531, 's_high': 107.91999816894531, 's_low': 107.91999816894531, 's_open': 107.91999816894531, 's_volume': 0.0, 'symbol': 'AAPL', 'timestamp': '2020-09-24T14:37:44.181335', 'updated_at': '2020-09-24T14:37:44.181335'}]
        self.assertEqual(body["data"], expected_response)

    