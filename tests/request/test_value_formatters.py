from assertpy import assert_that

from query_sentinel_products.request.value_formatters import (
    format_footprint,
    format_number_or_range,
)


class TestValueFormatters:
    def test_when_format_footprint_point_without_intersects_then_returns_correct_value(
        self,
    ):
        result = format_footprint("0 0")

        assert_that(result).is_equal_to('"Intersects(0 0)"')

    def test_when_format_footprint_polygon_no_intersects_then_returns_correct_value(
        self,
    ):
        result = format_footprint("POLYGON ((40 0, 40 20, 30 20, 40 0))")

        assert_that(result).is_equal_to(
            '"Intersects(POLYGON ((40 0, 40 20, 30 20, 40 0)))"'
        )

    def test_when_format_footprint_point_with_intersects_then_returns_correct_value(
        self,
    ):
        result = format_footprint("Intersects(1 0)")

        assert_that(result).is_equal_to('"Intersects(1 0)"')

    def test_when_format_footprint_polygon_with_intersects_then_returns_correct_value(
        self,
    ):
        result = format_footprint('"Intersects(POLYGON ((40 0, 40 20, 30 20, 40 0)))"')

        assert_that(result).is_equal_to(
            '"Intersects(POLYGON ((40 0, 40 20, 30 20, 40 0)))"'
        )

    def test_when_format_number_or_range_called_with_int_then_returns_value_as_string(
        self,
    ):
        result = format_number_or_range(24)

        assert_that(result).is_equal_to("24")

    def test_when_format_number_or_range_called_with_numeric_string_then_returns_value(
        self,
    ):
        result = format_number_or_range("245")

        assert_that(result).is_equal_to("245")

    def test_when_format_number_or_range_called_with_correct_range_then_returns_value(
        self,
    ):
        result = format_number_or_range("[35 TO 45]")

        assert_that(result).is_equal_to("[35 TO 45]")

    def test_when_format_number_or_range_range_without_brackets_then_adds_brackets(
        self,
    ):
        result = format_number_or_range("350 TO 405")

        assert_that(result).is_equal_to("[350 TO 405]")
