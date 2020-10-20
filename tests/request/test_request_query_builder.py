from unittest.mock import Mock, call, patch

from assertpy import assert_that

from query_sentinel_products import (
    OrbitDirection,
    PlatformName,
    PolarisationMode,
    RequestQueryBuilder,
    SensorOperationalMode,
    Sentinel1ProductType,
    SwathIdentifier,
    Timeliness,
    range_value,
)


class TestRequestQueryBuilder:
    def test_when_range_value_called_with_strings_supplied_then_creates_value_correctly(
        self,
    ):
        result = range_value("2020-10-15", "2020-12-13")

        assert_that(result).is_equal_to("[2020-10-15 TO 2020-12-13]")

    def test_when_empty_builder_initialised_supplied_then_build_returns_asterix(self):
        builder = RequestQueryBuilder()

        assert_that(builder.build()).is_equal_to("*")

    def test_when_platform_name_supplied_then_returns_correct_query_string(self,):
        builder = RequestQueryBuilder().platform_name(PlatformName.SENTINEL_1)

        assert_that(builder.build()).is_equal_to("platformname:Sentinel-1")

    def test_when_begin_position_supplied_then_returns_correct_query_string(self,):
        builder = RequestQueryBuilder().begin_position(
            "2020-01-01T00:00:00.000Z", "2020-02-01T00:00:00.000Z"
        )

        assert_that(builder.build()).is_equal_to(
            "beginposition:[2020-01-01T00:00:00.000Z TO 2020-02-01T00:00:00.000Z]"
        )

    @patch("query_sentinel_products.request.request_query_builder.date_value_validator")
    def test_when_begin_position_supplied_then_validates_both_start_and_end_date(
        self, date_value_validator_mock
    ):
        date_value_validator_mock.return_value = "2020-01-01T00:00:00.000Z"

        RequestQueryBuilder().begin_position(
            "2020-01-01T00:00:00.000Z", "2020-02-01T00:00:00.000Z"
        ).build()

        assert_that(date_value_validator_mock.call_count).is_equal_to(2)
        date_value_validator_mock.assert_has_calls(
            [call("2020-01-01T00:00:00.000Z"), call("2020-02-01T00:00:00.000Z")]
        )

    def test_when_invalid_begin_position_supplied_then_raises_value_error(self,):
        expected_error = (
            "begin_position_start and begin_position_end need to be a full ISO date "
            "or timestamp relative to now"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.begin_position).raises(ValueError).when_called_with(
            "NOT A DATE", "NOW"
        ).is_equal_to(expected_error)

    def test_when_end_position_supplied_then_returns_correct_query_string(self,):
        builder = RequestQueryBuilder().end_position(
            "2020-03-01T00:00:00.000Z", "2020-04-01T00:00:00.000Z"
        )

        assert_that(builder.build()).is_equal_to(
            "endposition:[2020-03-01T00:00:00.000Z TO 2020-04-01T00:00:00.000Z]"
        )

    @patch("query_sentinel_products.request.request_query_builder.date_value_validator")
    def test_when_end_position_supplied_then_validates_both_start_and_end_date(
        self, date_value_validator_mock
    ):
        date_value_validator_mock.return_value = "2020-01-01T00:00:00.000Z"

        RequestQueryBuilder().end_position(
            "2020-03-01T00:00:00.000Z", "2020-04-01T00:00:00.000Z"
        )

        assert_that(date_value_validator_mock.call_count).is_equal_to(2)
        date_value_validator_mock.assert_has_calls(
            [call("2020-03-01T00:00:00.000Z"), call("2020-04-01T00:00:00.000Z")]
        )

    def test_invalid_end_position_supplied_then_raises_value_error(self):
        expected_error = (
            "end_position_start and end_position_end need to be a full ISO date or "
            "timestamp relative to now"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.end_position).raises(ValueError).when_called_with(
            "NOT A DATE", "NOW"
        ).is_equal_to(expected_error)

    def test_when_ingestion_date_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().ingestion_date(
            "2020-05-01T00:00:00.000Z", "2020-06-01T00:00:00.000Z"
        )

        assert_that(builder.build()).is_equal_to(
            "ingestiondate:[2020-05-01T00:00:00.000Z TO 2020-06-01T00:00:00.000Z]"
        )

    @patch("query_sentinel_products.request.request_query_builder.date_value_validator")
    def test_when_ingestion_date_supplied_then_validates_both_start_and_end_date(
        self, date_value_validator_mock
    ):
        date_value_validator_mock.return_value = "2020-01-01T00:00:00.000Z"

        RequestQueryBuilder().ingestion_date(
            "2020-03-01T00:00:00.000Z", "2020-04-01T00:00:00.000Z"
        )

        assert_that(date_value_validator_mock.call_count).is_equal_to(2)
        date_value_validator_mock.assert_has_calls(
            [call("2020-03-01T00:00:00.000Z"), call("2020-04-01T00:00:00.000Z")]
        )

    def test_invalid_ingestion_date_supplied_then_raises_value_error(self):
        expected_error = (
            "ingestion_date_start and ingestion_date_end need to be a full ISO date "
            "or timestamp relative to now"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.ingestion_date).raises(ValueError).when_called_with(
            "NOT A DATE", "NOW"
        ).is_equal_to(expected_error)

    def test_when_collection_supplied_then_returns_correct_value(self):
        builder = RequestQueryBuilder().collection("CollectionA")

        assert_that(builder.build()).is_equal_to("collection:CollectionA")

    @patch(
        (
            "query_sentinel_products.request.request_query_builder."
            "string_not_empty_validator"
        )
    )
    def test_when_collection_supplied_then_validates_collection(
        self, string_not_empty_validator_mock
    ):
        string_not_empty_validator_mock.return_value = "12345"

        RequestQueryBuilder().collection("CollectionA")

        string_not_empty_validator_mock.assert_called_once_with("CollectionA")

    def test_when_empty_collection_supplied_then_raises_value_error(self):
        builder = RequestQueryBuilder()

        assert_that(builder.collection).raises(ValueError).when_called_with(
            ""
        ).is_equal_to("collection should not be empty")

    def test_when_file_name_supplied_then_returns_correct_value(self):
        builder = RequestQueryBuilder().file_name("filename13")

        assert_that(builder.build()).is_equal_to("filename:filename13")

    @patch(
        (
            "query_sentinel_products.request.request_query_builder."
            "string_not_empty_validator"
        )
    )
    def test_when_file_name_supplied_then_validates_supplied_value(
        self, string_not_empty_validator_mock
    ):
        string_not_empty_validator_mock.return_value = "12345"

        RequestQueryBuilder().file_name("Filename")

        string_not_empty_validator_mock.assert_called_once_with("Filename")

    def test_when_invalid_file_name_supplied_then_raises_value_error(self):
        builder = RequestQueryBuilder()

        assert_that(builder.file_name).raises(ValueError).when_called_with(
            "  "
        ).is_equal_to("filename should not be empty")

    def test_when_footprint_supplied_then_returns_correct_value(self):
        builder = RequestQueryBuilder().footprint("0 0")

        assert_that(builder.build()).is_equal_to('footprint:"Intersects(0 0)"')

    @patch(
        "query_sentinel_products.request.request_query_builder.geometry_type_validator"
    )
    def test_when_footprint_supplied_then_validates_supplied_footprint(
        self, geometry_type_validator_mock
    ):
        geometry_type_validator_mock.return_value = "1 1"

        RequestQueryBuilder().footprint("Intersects(1 1)")

        geometry_type_validator_mock.assert_called_once_with('"Intersects(1 1)"')

    @patch("query_sentinel_products.request.request_query_builder.format_footprint")
    def test_when_footprint_supplied_then_formats_matches_api_format(
        self, format_footprint_mock
    ):
        format_footprint_mock.return_value = '"Intersects(0 0)"'

        RequestQueryBuilder().footprint("0 0")

        format_footprint_mock.assert_called_once_with("0 0")

    def test_when_invalid_footprint_supplied_then_raises_value_error(self):
        expected_error = (
            "footprint must be called with valid geometry type - coordinate pair or "
            "simple polygon"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.footprint).raises(ValueError).when_called_with(
            "NOT VALID"
        ).is_equal_to(expected_error)

    def test_when_numeric_orbit_number_value_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().orbit_number(123)

        assert_that(builder.build()).is_equal_to("orbitnumber:123")

    def test_when_string_orbit_number_value_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().orbit_number("[1234 TO 12345]")

        assert_that(builder.build()).is_equal_to("orbitnumber:[1234 TO 12345]")

    @patch(
        "query_sentinel_products.request.request_query_builder.orbit_number_validator"
    )
    def test_when_orbit_number_supplied_then_validates_value(
        self, orbit_number_validator_mock
    ):
        orbit_number_validator_mock.return_value = "123"

        RequestQueryBuilder().orbit_number(123)

        orbit_number_validator_mock.assert_called_once_with("123")

    @patch(
        "query_sentinel_products.request.request_query_builder.format_number_or_range"
    )
    def test_when_orbit_number_supplied_then_formats_value(
        self, format_orbit_number_mock
    ):
        format_orbit_number_mock.return_value = "123"

        RequestQueryBuilder().orbit_number(123)

        format_orbit_number_mock.assert_called_once_with(123)

    def test_when_invalid_orbit_number_supplied_then_raises_value_error(self,):
        builder = RequestQueryBuilder()

        assert_that(builder.orbit_number).raises(ValueError).when_called_with(
            ""
        ).is_equal_to(
            "orbitnumber must be a range or single numeric value between 1 and 999999"
        )

    def test_when_numeric_last_orbit_number_value_supplied_then_returns_correct_value(
        self,
    ):
        builder = RequestQueryBuilder().last_orbit_number(123)

        assert_that(builder.build()).is_equal_to("lastorbitnumber:123")

    def test_when_string_last_orbit_number_value_supplied_then_returns_correct_value(
        self,
    ):
        builder = RequestQueryBuilder().last_orbit_number("[1234 TO 12345]")

        assert_that(builder.build()).is_equal_to("lastorbitnumber:[1234 TO 12345]")

    @patch(
        "query_sentinel_products.request.request_query_builder.orbit_number_validator"
    )
    def test_when_last_orbit_number_supplied_then_validates_value_supplied(
        self, orbit_number_validator_mock
    ):
        orbit_number_validator_mock.return_value = "1234"

        RequestQueryBuilder().last_orbit_number("1234")

        orbit_number_validator_mock.assert_called_once_with("1234")

    @patch(
        "query_sentinel_products.request.request_query_builder.format_number_or_range"
    )
    def test_when_last_orbit_number_supplied_then_formats_compatible_with_api(
        self, format_orbit_number_mock
    ):
        format_orbit_number_mock.return_value = "1234"

        RequestQueryBuilder().last_orbit_number(1234)

        format_orbit_number_mock.assert_called_once_with(1234)

    def test_when_invalid_last_orbit_number_supplied_then_raises_value_error(self,):
        expected_error = (
            "lastorbitnumber must be a range or single numeric value between "
            "1 and 999999"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.last_orbit_number).raises(ValueError).when_called_with(
            ""
        ).is_equal_to(expected_error)

    def test_when_numeric_relative_orbit_number_value_supplied_then_returns_correct_value(  # noqa E501
        self,
    ):
        builder = RequestQueryBuilder().relative_orbit_number(123)

        assert_that(builder.build()).is_equal_to("relativeorbitnumber:123")

    def test_when_string_relative_orbit_number_value_supplied_then_returns_correct_value(  # noqa E501
        self,
    ):
        builder = RequestQueryBuilder().relative_orbit_number("[1 TO 150]")

        assert_that(builder.build()).is_equal_to("relativeorbitnumber:[1 TO 150]")

    @patch(
        (
            "query_sentinel_products.request.request_query_builder."
            "relative_orbit_number_validator"
        )
    )
    def test_when_relative_orbit_number_supplied_then_validates_value_supplied(
        self, relative_orbit_number_validator_mock
    ):
        relative_orbit_number_validator_mock.return_value = "1"

        RequestQueryBuilder().relative_orbit_number("1")

        relative_orbit_number_validator_mock.assert_called_once_with("1")

    @patch(
        "query_sentinel_products.request.request_query_builder.format_number_or_range"
    )
    def test_when_relative_orbit_number_supplied_then_formats__compatible_with_api(
        self, format_orbit_number_mock
    ):
        format_orbit_number_mock.return_value = "123"

        RequestQueryBuilder().relative_orbit_number(123)

        format_orbit_number_mock.assert_called_once_with(123)

    def test_when_invalid_relative_orbit_number_supplied_then_raises_value_error(self,):
        expected_error = (
            "relativeorbitnumber must be a range or single numeric value between "
            "1 and 175"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.relative_orbit_number).raises(ValueError).when_called_with(
            10000
        ).is_equal_to(expected_error)

    def test_when_numeric_relative_last_orbit_number_value_then_returns_correct_value(
        self,
    ):
        builder = RequestQueryBuilder().last_relative_orbit_number(123)

        assert_that(builder.build()).is_equal_to("lastrelativeorbitnumber:123")

    def test_when_string_relative_last_orbit_number_value_then_returns_correct_value(
        self,
    ):
        builder = RequestQueryBuilder().last_relative_orbit_number("[123 TO 124]")

        assert_that(builder.build()).is_equal_to("lastrelativeorbitnumber:[123 TO 124]")

    @patch(
        (
            "query_sentinel_products.request.request_query_builder."
            "relative_orbit_number_validator"
        )
    )
    def test_when_relative_last_orbit_number_supplied_then_validates_value_supplied(
        self, relative_orbit_number_validator_mock
    ):
        relative_orbit_number_validator_mock.return_value = "124"

        RequestQueryBuilder().relative_orbit_number("123")

        relative_orbit_number_validator_mock.assert_called_once_with("123")

    @patch(
        "query_sentinel_products.request.request_query_builder.format_number_or_range"
    )
    def test_when_relative_last_orbit_number_supplied_then_value_compatible_with_api(
        self, format_orbit_number_mock
    ):
        format_orbit_number_mock.return_value = "123"

        RequestQueryBuilder().last_orbit_number(123)

        format_orbit_number_mock.assert_called_once_with(123)

    def test_when_invalid_relative_last_orbit_number_then_raises_value_error(self,):
        expected_error = (
            "lastrelativeorbitnumber must be a range or single numeric value between "
            "1 and 175"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.last_relative_orbit_number).raises(
            ValueError
        ).when_called_with("1000").is_equal_to(expected_error)

    def test_when_orbit_direction_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().orbit_direction(OrbitDirection.ASCENDING)

        assert_that(builder.build()).is_equal_to("orbitdirection:Ascending")

    def test_when_polarisation_mode_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().polarisation_mode(PolarisationMode.VV_VH)

        assert_that(builder.build()).is_equal_to("polarisationmode:VV VH")

    def test_when_product_type_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().product_type(Sentinel1ProductType.SLC)

        assert_that(builder.build()).is_equal_to("producttype:SLC")

    def test_when_sensor_operational_mode_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().sensor_operational_mode(
            SensorOperationalMode.EW
        )

        assert_that(builder.build()).is_equal_to("sensoroperationalmode:EW")

    def test_when_swath_identifier_supplied_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().swath_identifier(SwathIdentifier.S1)

        assert_that(builder.build()).is_equal_to("swathidentifier:S1")

    def test_when_numeric_cloud_cover_percentage_value_then_returns_correct_value(
        self,
    ):
        builder = RequestQueryBuilder().cloud_cover_percentage(23)

        assert_that(builder.build()).is_equal_to("cloudcoverpercentage:23")

    def test_when_string_cloud_cover_percentage_value_then_returns_correct_value(self,):
        builder = RequestQueryBuilder().cloud_cover_percentage("[20 TO 25]")

        assert_that(builder.build()).is_equal_to("cloudcoverpercentage:[20 TO 25]")

    @patch(
        (
            "query_sentinel_products.request.request_query_builder."
            "cloud_coverage_percentage_validator"
        )
    )
    def test_when_cloud_cover_percentage_supplied_then_validates_value_supplied(
        self, cloud_coverage_percentage_validator_mock
    ):
        cloud_coverage_percentage_validator_mock.return_value = "100"

        RequestQueryBuilder().cloud_cover_percentage(100)

        cloud_coverage_percentage_validator_mock.assert_called_once_with("100")

    @patch(
        "query_sentinel_products.request.request_query_builder.format_number_or_range"
    )
    def test_when_cloud_cover_percentage_supplied_then_formats_value_supplied(
        self, format_number_or_range_mock
    ):
        format_number_or_range_mock.return_value = "100"

        RequestQueryBuilder().cloud_cover_percentage(100)

        format_number_or_range_mock.assert_called_once_with(100)

    def test_when_invalid_cloud_cover_percentage_supplied_then_raises_value_error(
        self,
    ):
        expected_error = (
            "cloudcoverpercentage must be valid integral percentage number or range "
            "between 0 and 100"
        )
        builder = RequestQueryBuilder()

        assert_that(builder.cloud_cover_percentage).raises(ValueError).when_called_with(
            101
        ).is_equal_to(expected_error)

    def test_when_timeliness_supplied_then_returns_correct_value(self):
        builder = RequestQueryBuilder().timeliness(Timeliness.NRT)

        assert_that(builder.build()).is_equal_to("timeliness:NRT")

    def test_when_building_query_with_and_clauses_then_query_built_correctly(self):
        expected_query_value = (
            "platformname:Sentinel-1 AND cloudcoverpercentage:[10 TO 20] "
            'AND footprint:"Intersects(0 0)"'
        )
        builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .cloud_cover_percentage("10 TO 20")
            .and_()
            .footprint("0 0")
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_query_value)

    def test_when_building_query_with_or_clauses_then_query_built_correctly(self):
        expected_query = (
            "platformname:Sentinel-1 OR cloudcoverpercentage:[10 TO 20] "
            'OR footprint:"Intersects(0 0)"'
        )
        builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .or_()
            .cloud_cover_percentage("10 TO 20")
            .or_()
            .footprint("0 0")
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_query)

    def test_when_building_query_with_not_clause_then_query_built_correctly(self):
        builder = RequestQueryBuilder().not_().platform_name(PlatformName.SENTINEL_1)

        result = builder.build()

        assert_that(result).is_equal_to("NOT platformname:Sentinel-1")

    def test_when_query_with_and_or_and_not_clauses_then_query_built_correctly(self,):
        expected_result = (
            "NOT platformname:Sentinel-1 AND cloudcoverpercentage:[10 TO 20] "
            'OR footprint:"Intersects(0 0)"'
        )
        builder = (
            RequestQueryBuilder()
            .not_()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .cloud_cover_percentage("10 TO 20")
            .or_()
            .footprint("0 0")
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_result)

    def test_when_and_operator_trailing_then_does_not_have_operator_at_end(self,):
        expected_result = (
            "platformname:Sentinel-1 AND cloudcoverpercentage:[10 TO 20] AND "
            'footprint:"Intersects(0 0)"'
        )
        builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .cloud_cover_percentage("10 TO 20")
            .and_()
            .footprint("0 0")
            .and_()
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_result)

    def test_when_building_query_and_operator_called_first_then_removes_first_operator(
        self,
    ):
        expected_result = (
            "platformname:Sentinel-1 AND cloudcoverpercentage:[10 TO 20] "
            'AND footprint:"Intersects(0 0)"'
        )

        builder = (
            RequestQueryBuilder()
            .and_()
            .platform_name(PlatformName.SENTINEL_1)
            .and_()
            .cloud_cover_percentage("10 TO 20")
            .and_()
            .footprint("0 0")
            .and_()
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_result)

    def test_when_group_supplied_with_builder_supplied_then_calls_build(self):
        mock_builder = Mock(wraps=RequestQueryBuilder())

        RequestQueryBuilder().group_(mock_builder)

        mock_builder.build.assert_called_once()

    def test_when_group_called_supplied_then_adds_grouped_query(self):
        inner_builder = (
            RequestQueryBuilder().footprint("0 0").and_().cloud_cover_percentage("5")
        )

        expected_result = (
            '(footprint:"Intersects(0 0)" AND cloudcoverpercentage:5) OR '
            "platformname:Sentinel-1"
        )

        builder = (
            RequestQueryBuilder()
            .group_(inner_builder)
            .or_()
            .platform_name(PlatformName.SENTINEL_1)
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_result)

    def test_when_building_query_supplied_then_group_can_be_negated(self):
        inner_builder = (
            RequestQueryBuilder().footprint("0 0").and_().cloud_cover_percentage("5")
        )

        builder = RequestQueryBuilder().not_().group_(inner_builder)

        result = builder.build()

        assert_that(result).is_equal_to(
            'NOT (footprint:"Intersects(0 0)" AND cloudcoverpercentage:5)'
        )

    def test_when_no_operator_specified_between_two_filtera_then_defaults_to_and(self):

        expected_result = (
            "platformname:Sentinel-1 AND cloudcoverpercentage:[10 TO 20] "
            'AND footprint:"Intersects(0 0)"'
        )
        builder = (
            RequestQueryBuilder()
            .platform_name(PlatformName.SENTINEL_1)
            .cloud_cover_percentage("10 TO 20")
            .footprint("0 0")
        )

        result = builder.build()

        assert_that(result).is_equal_to(expected_result)
