from assertpy import assert_that, soft_assertions

from query_sentinel_products.request.validate_query_builder_args import (
    cloud_coverage_percentage_validator,
    geometry_type_validator,
    orbit_number_validator,
    relative_orbit_number_validator,
    string_not_empty_validator,
    validate_date_value,
)


class TestValidateQueryBuilderArgs:
    def test_when_validate_date_and_timestamp_in_iso_format_then_returns_date_val(
        self,
    ):
        date_val = "2020-01-01T00:00:00.000Z"

        result = validate_date_value(date_val)

        assert_that(result).is_not_none().is_equal_to(date_val)

    def test_when_validate_date_and_relative_date_then_returns_date_val(self):
        date_vals = [
            "NOW",
            "NOW-1HOUR",
            "NOW-2HOURS",
            "NOW-13HOURS",
            "NOW-1DAY",
            "NOW-2DAYS",
            "NOW-12DAYS",
        ]

        with soft_assertions():
            for date_val in date_vals:
                assert_that(validate_date_value(date_val)).is_equal_to(date_val)

    def test_when_validate_date_supplied_with_invalid_value_then_returns_none(self):
        date_vals = [
            "2020-01-01",
            "10/01/2002",
            "2019-01-01T11:00:00Z",
            "NOW+2DAYS",
            "2",
            "NotevenaDate",
        ]

        with soft_assertions():
            for date_val in date_vals:
                assert_that(validate_date_value(date_val)).is_none()

    def test_when_string_not_empty_validator_non_empty_string_then_returns_input(self,):
        str_val = "Not Empty"

        result = string_not_empty_validator(str_val)

        assert_that(result).is_not_none().is_equal_to(str_val)

    def test_when_string_not_empty_validator_empty_string_then_returns_none(self,):
        result = string_not_empty_validator("")

        assert_that(result).is_none()

    def test_when_string_not_empty_validator_only_whitespace_then_returns_none(self,):
        result = string_not_empty_validator("      ")

        assert_that(result).is_none()

    def test_when_geometry_type_validator_called_with_point_then_returns_str(self):
        result = geometry_type_validator('"Intersects(0 0)"')

        assert_that(result).is_equal_to('"Intersects(0 0)"')

    def test_when_geometry_type_validator_point_without_intersects_then_returns_none(
        self,
    ):
        result = geometry_type_validator("0 0")

        assert_that(result).is_none()

    def test_when_geometry_type_validator_called_with_polygon_then_returns_str(self):
        result = geometry_type_validator(
            '"Intersects(POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10)))"'
        )

        assert_that(result).is_equal_to(
            '"Intersects(POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10)))"'
        )

    def test_when_geometry_type_validator_polygon_without_intersects_then_returns_none(
        self,
    ):
        result = geometry_type_validator(
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
        )

        assert_that(result).is_none()

    def test_when_geometry_type_validator_polygon_with_hole_then_returns_none(self,):
        polygon = (
            '"Intersects(POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), '
            '(20 30, 35 35, 30 20, 20 30)))"'
        )
        result = geometry_type_validator(polygon)

        assert_that(result).is_none()

    def test_when_geometry_type_validator_called_with_multipolygon_then_returns_none(
        self,
    ):
        multipolygon = (
            '"Intersects(MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), '
            '((15 5, 40 10, 10 20, 5 10, 15 5))))"'
        )
        result = geometry_type_validator(multipolygon)

        assert_that(result).is_none()

    def test_when_geometry_type_validator_empty_str_then_returns_none(self):
        result = geometry_type_validator("")

        assert_that(result).is_none()

    def test_when_geometry_type_validator_non_geometry_string_then_returns_none(self,):
        result = geometry_type_validator(
            "Not POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10)) or Point"
        )

        assert_that(result).is_none()

    def test_when_orbit_number_validator_numeric_value_then_it_returns_value(self,):
        result = orbit_number_validator("21")

        assert_that(result).is_equal_to("21")

    def test_when_orbit_number_validator_numeric_range_string_then_returns_value(self,):
        result = orbit_number_validator("[1234 TO 4321]")

        assert_that(result).is_equal_to("[1234 TO 4321]")

    def test_when_orbit_number_validator_empty_string_then_returns_none(self,):
        result = orbit_number_validator("")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_non_numberic_range_then_returns_none(self,):
        result = orbit_number_validator("[NOT TO RANGE]")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_range_missing_braces_then_returns_none(self,):
        result = orbit_number_validator("1234 TO 4321")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_number_too_large_then_returns_none(self,):
        result = orbit_number_validator("1000000")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_range_with_large_numbers_then_returns_none(
        self,
    ):
        result = orbit_number_validator("[1000000 TO 1000001]")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_negative_number_then_returns_none(self,):
        result = orbit_number_validator("-1000")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_range_of_negative_numbers_then_returns_none(
        self,
    ):
        result = orbit_number_validator("[-1000 TO 1000]")

        assert_that(result).is_none()

    def test_when_orbit_number_validator_supplied_with_zero_then_returns_none(self):
        result = orbit_number_validator("0")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_numeric_value_then_it_returns_value(
        self,
    ):
        result = relative_orbit_number_validator("21")

        assert_that(result).is_equal_to("21")

    def test_when_relative_orbit_number_validator_numeric_range_then_returns_value(
        self,
    ):
        result = relative_orbit_number_validator("[31 TO 21]")

        assert_that(result).is_equal_to("[31 TO 21]")

    def test_when_relative_orbit_number_validator_empty_string_then_returns_none(self,):
        result = relative_orbit_number_validator("")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_non_numberic_range_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("[NOT TO RANGE]")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_range_no_braces_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("32 TO 22")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_number_too_large_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("176")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_range_large_number_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("[176 TO 177]")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_negative_number_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("-1")

        assert_that(result).is_none()

    def test_when_rel_orbit_number_validator_range_negative_number_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("[-1 TO 170]")

        assert_that(result).is_none()

    def test_when_relative_orbit_number_validator_supplied_with_zero_then_returns_none(
        self,
    ):
        result = relative_orbit_number_validator("0")

        assert_that(result).is_none()

    def test_when_cloud_coverage_percentage_validator_numeric_value_then_returns_value(
        self,
    ):
        result = cloud_coverage_percentage_validator("10")

        assert_that(result).is_equal_to("10")

    def test_when_cloud_coverage_percentage_validator_range_then_returns_value(self,):
        result = cloud_coverage_percentage_validator("[10 TO 20]")

        assert_that(result).is_equal_to("[10 TO 20]")

    def test_when_cloud_cover_percentage_validator_fraction_perc_then_returns_none(
        self,
    ):
        result = cloud_coverage_percentage_validator("10.234")

        assert_that(result).is_none()

    def test_when_cloud_coverage_percentage_validator_large_value_then_returns_none(
        self,
    ):
        result = cloud_coverage_percentage_validator("101")

        assert_that(result).is_none()

    def test_when_cloud_cover_percentage_validator_range_large_value_then_returns_none(
        self,
    ):
        result = cloud_coverage_percentage_validator("[101 TO 102]")

        assert_that(result).is_none()
