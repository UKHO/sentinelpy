import json
import logging
import re
from os import getcwd

import requests
import responses
from assertpy import assert_that

from sentinelpy import (
    PlatformName,
    RequestQueryBuilder,
    Sentinel1ProductType,
    SentinelProductRequestBuilder,
    query_sentinel_hub,
)
from tests.utils import get_query_parameters_of_url

DATA_DIR = f"{getcwd()}/tests/data" if "tests" not in getcwd() else f"{getcwd()}/data"


class TestQuerySentinelProducts:
    @responses.activate
    def test_when_successful_request_made_then_returns_products(self):
        expected_query_parameters = {
            "q": ["platformname:Sentinel-1 AND producttype:GRD"],
            "start": ["0"],
            "rows": ["30"],
            "format": ["json"],
        }

        with open(f"{DATA_DIR}/sentinel.api.json", "r") as sentinel_data:
            json_data = sentinel_data.read()

        sentinel_data = json.loads(json_data)

        responses.add(
            responses.GET,
            re.compile(r"https://scihub\.copernicus\.eu/dhus/.+"),
            json=sentinel_data,
            status=200,
        )

        query_builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .product_type(Sentinel1ProductType.GRD)
        )
        request = (
            SentinelProductRequestBuilder()
            .with_rows(30)
            .with_username("test-user")
            .with_password("test-password")
            .with_query(query_builder)
        )

        result = query_sentinel_hub(request.build(), log_level=logging.DEBUG)

        assert_that(result.success).is_true()
        assert_that(result.body).is_equal_to(sentinel_data)

        url = responses.calls[0].request.url

        assert_that(get_query_parameters_of_url(url)).is_equal_to(
            expected_query_parameters
        )
        assert_that(url).starts_with("https://scihub.copernicus.eu/dhus/search?")

    @responses.activate
    def test_when_failure_response_from_sentinel_hub_then_returns_failure(self):
        expected_query_parameters = {
            "q": [
                "platformname:Sentinel-1 AND producttype:GRD AND NOT "
                "(cloudcoverpercentage:[5 TO 10] OR cloudcoverpercentage:[45 TO 50])"
            ],
            "start": ["0"],
            "rows": ["30"],
            "format": ["json"],
        }

        responses.add(
            responses.GET,
            re.compile(r"https://scihub\.copernicus\.eu/dhus/.+"),
            body="<html></html>",
            status=401,
        )
        query_builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .product_type(Sentinel1ProductType.GRD)
            .and_()
            .not_()
            .group_(
                RequestQueryBuilder()
                .cloud_cover_percentage("5 TO 10")
                .or_()
                .cloud_cover_percentage("[45 TO 50]")
            )
        )
        request = (
            SentinelProductRequestBuilder()
            .with_rows(30)
            .with_username("test-user")
            .with_password("test-password")
            .with_query(query_builder)
        )

        result = query_sentinel_hub(request.build(), log_level=logging.DEBUG)

        assert_that(result.success).is_false()
        assert_that(result.status_code).is_equal_to(401)

        url = responses.calls[0].request.url

        assert_that(get_query_parameters_of_url(url)).is_equal_to(
            expected_query_parameters
        )
        assert_that(url).starts_with("https://scihub.copernicus.eu/dhus/search?")

    @responses.activate
    def test_when_error_when_calling_api_then_returns_error_result(self):
        error = requests.ConnectionError()

        responses.add(
            responses.GET,
            re.compile(r"https://scihub\.copernicus\.eu/dhus/.+"),
            body=error,
        )
        request = (
            SentinelProductRequestBuilder()
            .with_rows(30)
            .with_username("test-user")
            .with_password("test-password")
        )

        result = query_sentinel_hub(request.build(), log_level=logging.DEBUG)

        assert_that(result.success).is_false()
        assert_that(result.status_code).is_none()
        assert_that(result.body).is_none()
        assert_that(result.error).is_equal_to(error)
