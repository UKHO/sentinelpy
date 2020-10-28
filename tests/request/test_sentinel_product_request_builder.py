from assertpy import assert_that

from query_sentinel_products import (
    PlatformName,
    RequestQueryBuilder,
    SentinelProductRequest,
    SentinelProductRequestBuilder,
)


class TestSentinelProductRequestBuilder:
    def test_when_build_called_on_empty_builder_then_raises_value_error(self,):
        empty_builder = SentinelProductRequestBuilder()

        assert_that(empty_builder.build).raises(
            ValueError
        ).when_called_with().is_equal_to("username is required; password is required;")

    def test_when_no_query_then_request_has_query_with_default_value(self,):
        builder = (
            SentinelProductRequestBuilder(default_query="DEFAULT")
            .with_rows(10)
            .with_order_by("ordering")
            .with_start(10)
            .with_username("username")
            .with_password("password")
        )

        assert_that(builder.build().query).is_equal_to("DEFAULT")

    def test_when_no_rows_then_request_has_rows_is_none(self,):
        builder = (
            SentinelProductRequestBuilder()
            .with_query("*")
            .with_order_by("ordering")
            .with_start(10)
            .with_username("username")
            .with_password("password")
        )

        assert_that(builder.build().rows).is_none()

    def test_when_no_ordering_then_request_has_ordering_with_default_value(self,):
        builder = (
            SentinelProductRequestBuilder(default_order_by="DEFAULT")
            .with_rows(10)
            .with_query("*")
            .with_start(10)
            .with_username("username")
            .with_password("password")
        )

        assert_that(builder.build().order_by).is_equal_to("DEFAULT")

    def test_when_no_start_then_request_has_default_start(self,):
        builder = (
            SentinelProductRequestBuilder(default_start=10)
            .with_rows(10)
            .with_order_by("ordering")
            .with_query("*")
            .with_username("username")
            .with_password("password")
        )

        assert_that(builder.build().start).is_equal_to(10)

    def test_when_build_called_then_built_request_has_attributes_supplied(self):
        builder = (
            SentinelProductRequestBuilder()
            .with_query("platformname:Sentinel-1")
            .with_rows(30)
            .with_order_by("ingestiondate desc")
            .with_start(30)
            .with_username("username1")
            .with_password("password1")
        )

        expected_request = SentinelProductRequest(
            username="username1",
            password="password1",
            query="platformname:Sentinel-1",
            rows=30,
            order_by="ingestiondate desc",
            start=30,
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_request)

    def test_when_query_is_query_builder_then_calls_build_when_building_request(self):
        query_builder = RequestQueryBuilder().platform_name(PlatformName.SENTINEL_1)

        request_builder = (
            SentinelProductRequestBuilder()
            .with_query(query_builder)
            .with_rows(30)
            .with_order_by("ingestiondate desc")
            .with_username("username")
            .with_password("password")
        )

        result = request_builder.build()

        assert_that(result.query).is_equal_to("platformname:Sentinel-1")
