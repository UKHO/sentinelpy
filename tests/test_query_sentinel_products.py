from unittest.mock import Mock, patch

import pytest
from assertpy import assert_that

from query_sentinel_products import query
from query_sentinel_products.request import SentinelProductRequest


@pytest.fixture()
def requests_mock():
    with patch("query_sentinel_products.query_sentinel_products.requests") as mock:
        yield mock


class TestQuerySentinelProducts:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, requests_mock):
        self.requests_mock = requests_mock
        self.sentinel_product_request = SentinelProductRequest(
            "*", 30, None, 0, "test-user", "test-password"
        )
        self.ordered_sentinel_product_request = SentinelProductRequest(
            "*", 30, "beginposition asc", 0, "test-user", "test-password"
        )

    def test_when_called_then_calls_api(self):
        query(self.sentinel_product_request)

        self.requests_mock.get.assert_called_once()

    def test_when_query_called_then_calls_are_authenticated(self):
        query(self.sentinel_product_request)

        requests_call_kwargs = self.requests_mock.get.call_args.kwargs

        assert_that(requests_call_kwargs["auth"]).is_equal_to(
            ("test-user", "test-password")
        )

    def test_when_query_called_without_ordering_then_calls_correct_url(self):
        query(self.sentinel_product_request)

        requests_call_args = self.requests_mock.get.call_args.args

        assert_that(requests_call_args[0]).is_equal_to(
            "https://scihub.copernicus.eu/dhus/search?q=*&rows=30&start=0&format=json"
        )

    def test_when_query_called_with_ordering_then_calls_correct_url(self):
        query(self.ordered_sentinel_product_request)

        requests_call_args = self.requests_mock.get.call_args.args

        assert_that(requests_call_args[0]).is_equal_to(
            "https://scihub.copernicus.eu/dhus/search?q=*&rows=30&start=0&orderby=beginposition asc&format=json"
        )
