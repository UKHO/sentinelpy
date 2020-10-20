import json
import logging
import re
from os import getcwd

import requests
import responses
from assertpy import assert_that

from query_sentinel_products import (
    PlatformName,
    RequestQueryBuilder,
    Sentinel1ProductType,
    SentinelProductRequestBuilder,
    query_sentinel_hub,
)

DATA_DIR = f"{getcwd()}/tests/data" if "tests" not in getcwd() else f"{getcwd()}/data"


class TestQuerySentinelProducts:
    @responses.activate
    def test_when_successful_request_made_then_returns_products(self):
        expected_url = (
            "https://scihub.copernicus.eu/dhus/search?q=platformname:Sentinel-1%20"
            "AND%20producttype:GRD&rows=30&start=0&format=json"
        )

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
        assert_that(result.data).is_equal_to(sentinel_data)
        assert_that(responses.calls[0].request.url).is_equal_to(expected_url)

    @responses.activate
    def test_when_failure_response_from_sentinel_hub_then_returns_failure(self):
        expected_url = (
            "https://scihub.copernicus.eu/dhus/search?q=platformname:Sentinel-1"
            "%20AND%20producttype:GRD%20AND%20NOT%20(cloudcoverpercentage:"
            "%5B5%20TO%2010%5D%20OR%20cloudcoverpercentage:%5B45%20TO%2050%5D)"
            "&rows=30&start=0&format=json"
        )

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
        assert_that(responses.calls[0].request.url).is_equal_to(expected_url)

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
        assert_that(result.data).is_none()
        assert_that(result.error).is_equal_to(error)
