import logging
from unittest.mock import call, patch
from urllib.parse import parse_qs, parse_qsl, urlencode

import pytest
import requests
from assertpy import assert_that

from sentinelpy import SentinelProductRequest, query_sentinel_hub
from sentinelpy.exceptions import QuerySentinelProductsError
from sentinelpy.query_sentinel_products_response import QuerySentinelProductsResponse
from tests.utils import get_query_parameters_of_url


@pytest.fixture()
def requests_mock():
    with patch("sentinelpy.main.requests") as mock:
        yield mock


class TestQuerySentinelHub:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, requests_mock):
        self.requests_mock = requests_mock
        self.sentinel_product_request = SentinelProductRequest(
            "*", 30, None, 0, "test-user", "test-password"
        )
        self.sentinel_product_request_no_rows = SentinelProductRequest(
            "*", None, None, 0, "test-user", "test-password"
        )
        self.ordered_sentinel_product_request = SentinelProductRequest(
            "*", 30, "beginposition asc", 0, "test-user", "test-password"
        )
        self.sentinel_product_request_with_query = SentinelProductRequest(
            "platformname:Sentinel-1 AND cloudcoverpercentage:5",
            30,
            None,
            0,
            "test-user",
            "test-password",
        )

    def _get_called_url(self):

        calls = self.requests_mock.get.call_args_list

        assert_that(len(calls)).is_equal_to(1)

        call = calls[0]

        positional_args, _ = call
        return positional_args[0]

    def test_when_called_then_calls_api(self):
        query_sentinel_hub(self.sentinel_product_request)

        self.requests_mock.get.assert_called_once()

    def test_when_query_called_then_calls_are_authenticated(self):
        expected_auth = (
            self.sentinel_product_request.username,
            self.sentinel_product_request.password,
        )

        query_sentinel_hub(self.sentinel_product_request)

        calls = self.requests_mock.get.call_args_list

        assert_that(len(calls)).is_equal_to(1)

        call = calls[0]

        _, kwargs = call

        assert_that(kwargs["auth"]).is_equal_to(expected_auth)

    def test_when_query_called_without_ordering_then_calls_correct_url(self):
        expected_params = {
            "q": ["*"],
            "start": ["0"],
            "rows": ["30"],
            "format": ["json"],
        }

        query_sentinel_hub(self.sentinel_product_request)

        url = self._get_called_url()

        assert_that(get_query_parameters_of_url(url)).is_equal_to(expected_params)
        assert_that(url).starts_with("https://scihub.copernicus.eu/dhus/search?")

    def test_when_query_called_without_rows_then_calls_correct_url(self):
        expected_params = {"q": ["*"], "start": ["0"], "format": ["json"]}

        query_sentinel_hub(self.sentinel_product_request_no_rows)

        url = self._get_called_url()

        assert_that(get_query_parameters_of_url(url)).is_equal_to(expected_params)
        assert_that(url).starts_with("https://scihub.copernicus.eu/dhus/search?")

    def test_when_query_called_with_ordering_then_calls_correct_url(self):
        expected_params = {
            "q": ["*"],
            "start": ["0"],
            "format": ["json"],
            "orderby": ["beginposition asc"],
            "rows": ["30"],
        }

        query_sentinel_hub(self.ordered_sentinel_product_request)

        url = self._get_called_url()

        assert_that(get_query_parameters_of_url(url)).is_equal_to(expected_params)

    def test_when_query_supplied_then_the_url_contains_query(self):
        expected_params = {
            "q": ["platformname:Sentinel-1 AND cloudcoverpercentage:5"],
            "start": ["0"],
            "format": ["json"],
            "rows": ["30"],
        }

        query_sentinel_hub(self.sentinel_product_request_with_query)

        url = self._get_called_url()

        assert_that(get_query_parameters_of_url(url)).is_equal_to(expected_params)

    def test_when_request_successful_then_returns_status_code_and_json(self):
        self.requests_mock.get.return_value.status_code = 200
        self.requests_mock.get.return_value.json.return_value = {"content": {}}

        result = query_sentinel_hub(self.sentinel_product_request)

        assert_that(result).is_equal_to(
            QuerySentinelProductsResponse(200, {"content": {}}, None)
        )

    def test_when_request_has_non_200_status_code_then_returns_status_code_and_json(
        self,
    ):
        self.requests_mock.get.return_value.status_code = 400
        self.requests_mock.get.return_value.json.return_value = {"content": {}}

        result = query_sentinel_hub(self.sentinel_product_request)

        assert_that(result).is_equal_to(
            QuerySentinelProductsResponse(400, {"content": {}}, None)
        )

    def test_when_requests_raises_error_then_returns_error(self):
        error = requests.ConnectionError()
        self.requests_mock.get.side_effect = error

        result = query_sentinel_hub(self.sentinel_product_request)

        assert_that(result).is_equal_to(
            QuerySentinelProductsResponse(None, None, error)
        )

    def test_when_response_is_not_json_then_returns_content_as_string_with_error(self):
        original_error = ValueError()
        self.requests_mock.get.return_value.status_code = 200
        self.requests_mock.get.return_value.json.side_effect = original_error
        self.requests_mock.get.return_value.content = "Not json".encode()

        result = query_sentinel_hub(self.sentinel_product_request)

        assert_that(result).is_equal_to(
            QuerySentinelProductsResponse(
                200, None, QuerySentinelProductsError(original_error, 200, "Not json")
            )
        )

    @patch("sentinelpy.main.urlencode")
    def test_when_called_then_encodes_parameters(self, urlencode_mock):
        query_sentinel_hub(self.sentinel_product_request_with_query)

        urlencode_mock.assert_called_once_with(
            {
                "q": "platformname:Sentinel-1 AND cloudcoverpercentage:5",
                "start": 0,
                "format": "json",
                "rows": 30,
            }
        )

    @patch("sentinelpy.main.logging")
    def test_when_query_sentinel_hub_called_then_it_logs_at_the_set_log_level(
        self, logging_mock
    ):
        query_sentinel_hub(self.sentinel_product_request, log_level=logging.DEBUG)

        logging_mock.getLogger.assert_called_once()
        logging_mock.getLogger.return_value.setLevel.assert_called_once_with(
            logging.DEBUG
        )
