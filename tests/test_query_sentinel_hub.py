import logging
from unittest.mock import patch

import pytest
import requests
from assertpy import assert_that

from query_sentinel_products import SentinelProductRequest, query_sentinel_hub
from query_sentinel_products.exceptions import QuerySentinelProductsError
from query_sentinel_products.query_sentinel_products_response import (
    QuerySentinelProductsResponse,
)


@pytest.fixture()
def requests_mock():
    with patch("query_sentinel_products.main.requests") as mock:
        yield mock


class TestQuerySentinelHub:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, requests_mock):
        self.requests_mock = requests_mock
        self.sentinel_product_request = SentinelProductRequest(
            "*", 30, None, 0, "test-user", "test-password"
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

    def test_when_called_then_calls_api(self):
        query_sentinel_hub(self.sentinel_product_request)

        self.requests_mock.get.assert_called_once()

    def test_when_query_called_then_calls_are_authenticated(self):
        query_sentinel_hub(self.sentinel_product_request)

        requests_call_kwargs = self.requests_mock.get.call_args.kwargs

        assert_that(requests_call_kwargs["auth"]).is_equal_to(
            ("test-user", "test-password")
        )

    def test_when_query_called_without_ordering_then_calls_correct_url(self):
        query_sentinel_hub(self.sentinel_product_request)

        requests_call_args = self.requests_mock.get.call_args.args

        assert_that(requests_call_args[0]).is_equal_to(
            "https://scihub.copernicus.eu/dhus/search?q=*&rows=30&start=0&format=json"
        )

    def test_when_query_called_with_ordering_then_calls_correct_url(self):
        exected_url = (
            "https://scihub.copernicus.eu/dhus/search?q=*&"
            "rows=30&start=0&orderby=beginposition asc&format=json"
        )

        query_sentinel_hub(self.ordered_sentinel_product_request)

        requests_call_args = self.requests_mock.get.call_args.args

        assert_that(requests_call_args[0]).is_equal_to(exected_url)

    def test_when_query_supplied_then_the_url_contains_query(self):
        expected_url = (
            "https://scihub.copernicus.eu/dhus/search?"
            "q=platformname:Sentinel-1 AND cloudcoverpercentage:5"
            "&rows=30&start=0&format=json"
        )

        query_sentinel_hub(self.sentinel_product_request_with_query)

        requests_call_args = self.requests_mock.get.call_args.args

        assert_that(requests_call_args[0]).is_equal_to(expected_url)

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
        self.requests_mock.get.return_value.status_code = 200
        self.requests_mock.get.return_value.json.side_effect = ValueError()
        self.requests_mock.get.return_value.content = "Not json".encode()

        result = query_sentinel_hub(self.sentinel_product_request)

        assert_that(result).is_equal_to(
            QuerySentinelProductsResponse(
                200, None, QuerySentinelProductsError(ValueError(), 200, "Not json")
            )
        )

    @patch("query_sentinel_products.main.logging")
    def test_when_query_sentinel_hub_called_then_it_logs_at_the_set_log_level(
        self, logging_mock
    ):
        query_sentinel_hub(self.sentinel_product_request, log_level=logging.DEBUG)

        logging_mock.getLogger.assert_called_once()
        logging_mock.getLogger.return_value.setLevel.assert_called_once_with(
            logging.DEBUG
        )
