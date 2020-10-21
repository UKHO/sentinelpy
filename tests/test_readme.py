from unittest.mock import patch
import logging

from query_sentinel_products import (
    query_sentinel_hub,
	SentinelProductRequestBuilder, 
	RequestQueryBuilder,
	PlatformName,
    SentinelProductRequest,
    QuerySentinelProductsResponse,
    PolarisationMode,
    range_value
)


class TestReadme:
    
    @patch(
        "query_sentinel_products.main.query_sentinel_hub", 
        returnvalue=QuerySentinelProductsResponse(status_code=200, body={})
    )
    def test_usage_example(self, query_sentinel_hub_mock):
        request = (
            SentinelProductRequestBuilder()
            .with_username("username")
            .with_password("password")
            .with_query(
                RequestQueryBuilder()
                .platform_name(PlatformName.SENTINEL_1)
            )
            .build()
        )

        result = query_sentinel_hub(request, log_level=logging.DEBUG)

        assert isinstance(result, QuerySentinelProductsResponse)

    def test_range_value_example(self):
        query = (
            RequestQueryBuilder()
            .orbit_number(range_value("1", "2"))
            .build()
        )

        assert query == "orbitnumber:[1 TO 2]"

    def test_query_sentinel_products_response_examples(self):
        # You can use the attributes of the response in a more object fashion
        # Successful response:
        successful_response = QuerySentinelProductsResponse(200, {})

        assert successful_response.success == True
        assert successful_response.status_code == 200
        assert successful_response.body == {}
        assert successful_response.error == None

        # Failed response:
        failed_response = QuerySentinelProductsResponse(400, {})
        assert failed_response.success == False
        assert failed_response.status_code == 400
        assert failed_response.body == {}
        assert failed_response.error == None

        # Erroneous response
        error = IOError()
        erroneous_response = QuerySentinelProductsResponse(None, None, error)
        assert erroneous_response.success == False
        assert erroneous_response.status_code == None
        assert erroneous_response.body == None
        assert erroneous_response.error == error

        # Using the functional style methods
        successful_response.on_success(
            lambda data: print(f'success:{data}')
        ).on_failure(
            lambda failure_response: print(f'failure:{failure_response.status_code}')
        ) # success:{}

        failed_response.on_success(
            lambda data: print(f'success:{data}')
        ).on_failure(
            lambda failure_response: print(f'failure:{failure_response.status_code}')
        ) # failure:400


    def test_request_query_builder_examples(self):
        minimal = (
            SentinelProductRequestBuilder()
            .with_username("username")
            .with_password("password")
            .build()
        )

        assert minimal == SentinelProductRequest(
            query="*",
            rows=30,
            order_by=None,
            start=0,
            username="username",
            password="password"
        )

        full = (
            SentinelProductRequestBuilder()
            .with_username("username")
            .with_password("password")
            .with_query(RequestQueryBuilder().platform_name(PlatformName.SENTINEL_1))
            .with_start(15)
            .with_rows(15)
            .with_ordering('ingestiondate desc')
            .build()
        )

        assert full == SentinelProductRequest(
            query="platformname:Sentinel-1",
            rows=15,
            order_by='ingestiondate desc',
            start=15,
            username="username",
            password="password"
        )

    def test_request_query_builder_build_example(self):
        default_build_behaviour = RequestQueryBuilder().build()

        assert default_build_behaviour == "*"

        hanging_operator_start = RequestQueryBuilder().and_().platform_name(PlatformName.SENTINEL_1).build()

        assert hanging_operator_start == "platformname:Sentinel-1"

        hanging_operator_end = RequestQueryBuilder().not_().platform_name(PlatformName.SENTINEL_1).and_().build()

        assert hanging_operator_end == "NOT platformname:Sentinel-1"
    
    def test_request_query_builder_group_example(self):
        q = (
            RequestQueryBuilder()
            .group_(
                RequestQueryBuilder()
                .platform_name(PlatformName.SENTINEL_1)
                .and_()
                .polarisation_mode(PolarisationMode.HH)
            )
            .or_()
            .group_(
                RequestQueryBuilder()
                .platform_name(PlatformName.SENTINEL_1)
                .and_()
                .not_()
                .polarisation_mode(PolarisationMode.VH)
            )
            .build()
        )

        assert q == (
            "(platformname:Sentinel-1 AND polarisationmode:HH) OR "
            "(platformname:Sentinel-1 AND NOT polarisationmode:VH)"
        )
    
    def test_request_query_example(self):
        simple_q = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .build()
        )

        assert simple_q == "platformname:Sentinel-1"

        multiple_clauses_q = (
            RequestQueryBuilder()
                .platform_name(PlatformName.SENTINEL_3)
                .and_()
                .cloud_cover_percentage("[0 TO 5]")
                .and_()
                .footprint(
                    "POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.80,-4.53 46.80,-4.53 29.85))"
                )
                .build()
        )

        assert multiple_clauses_q == (
            'platformname:Sentinel-3 AND cloudcoverpercentage:[0 TO 5] AND '
            'footprint:"Intersects(POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.'
            '80,-4.53 46.80,-4.53 29.85)))"'
        )
