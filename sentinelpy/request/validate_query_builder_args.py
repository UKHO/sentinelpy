import re
from functools import reduce
from typing import Any, Optional

DATE_TIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
RELATIVE_DATE_PATTERN = re.compile(r"^NOW(?:-\d+(?:MINUTE|HOUR|DAY|MONTH)S?)?$")
INTERSECTS_PATTERN = re.compile(r"(?s)^\"Intersects\(.*")
POLYGON_PATTERN = re.compile(
    r"(?si).*POLYGON\s*\(\((\s*-?\d{1,3}\.?\d* -?\d{1,2}\.?\d*,?){3,}\)\)\)\"$"
)
POINT_PATTERN = re.compile(
    (
        r".*-?([1]?[1-7][1-9]|[1]?[1-8][0]|[1-9]?[0-9])\.?\d*,"
        r"\s*-?[0-9]{1,2}\.?\d*\)\"$"
    )
)


def date_value_validator(date_val: str) -> Optional[str]:
    """Validates the parameter to check it is valid date or not

    Args:
        date_val::str
            Value that could be a date that should be validated
    Returns:
        val::Optional[str]
            Validated date value - if present the value is valid
            if not present, the value is not valid
    """
    is_iso_timestamp = DATE_TIME_PATTERN.match(date_val) is not None
    is_relative_time = RELATIVE_DATE_PATTERN.match(date_val) is not None

    return date_val if is_iso_timestamp or is_relative_time else None


def string_not_empty_validator(str_val: str) -> Optional[str]:
    """Validates the parameter to check the string is not empty

    Args:
        str_val::str
            Value that could be empty

    Returns:
        val::Optional[str]
            Validated string value - if present the value is valid
            if not present, the value is not validated
    """
    is_only_whitespace = re.compile(r"^\s*$").match(str_val) is not None
    return str_val if str_val and not is_only_whitespace else None


def geometry_type_validator(str_val: str) -> Optional[str]:
    """Validates the parameter to check it is a valid geometry type - i.e. WKT string

    Args:
        str_val::str
            Value that could be a Geometry Type

    Returns:
        val::Optional[str]
            Validated string value - if value present the value is valid
            if not present, the value is not validated
    """
    has_intersects = INTERSECTS_PATTERN.match(str_val) is not None
    is_polygon = POLYGON_PATTERN.match(str_val) is not None
    is_point = POINT_PATTERN.match(str_val) is not None

    is_valid_geom = has_intersects and (is_point or is_polygon)

    return str_val if is_valid_geom else None


def orbit_number_validator(orbit_number: str) -> Optional[str]:
    """Validates the parameter to check whether it is a valid orbit number
    (1 To 999999)

    Args:
        orbit_number::str
            Value that could be orbit number either single value or a range

    Returns:
        val::Optional[str]
            Validated orbit number - if the value is valid - i.e. a numeric value or
            it is a valid range it returns the orbit number as a string otherwise
            returns None - it is invalid.
    """
    match = __number_or_range_pattern(6).match(orbit_number)
    return (
        orbit_number
        if match is not None and __all_values_in_range(match, 1, 999999)
        else None
    )


def relative_orbit_number_validator(orbit_number: str) -> Optional[str]:
    """Validate the supplied parameter to check whether it is a valid relative orbit
    number (1 To 175)

    Args:
        orbit_number::str
            Value that could be orbit number either single value or a range

    Returns:
        val::Optional[str]
            Validated orbit number - if the value is valid - i.e. a numeric value or
            it is a valid range it returns the orbit number as a string otherwise
            returns None - it is invalid.
    """
    match = __number_or_range_pattern(3).match(orbit_number)
    return (
        orbit_number
        if match is not None and __all_values_in_range(match, 1, 175)
        else None
    )


def cloud_coverage_percentage_validator(
    cloud_coverage_percentage: str,
) -> Optional[str]:
    """Validate the supplied parameter to check whether it is a valid percentage

       Args:
           cloud_coverage_percentage::str
               Value that could be percentage either single value or a range

       Returns:
           val::Optional[str]
               Validated percentage - if the value is valid - i.e. a numeric value or
               it is a valid range it returns the orbit number as a string otherwise
               returns None - it is invalid.
       """
    match = __number_or_range_pattern(3).match(cloud_coverage_percentage)

    return (
        cloud_coverage_percentage
        if match is not None and __all_values_in_range(match, 0, 100)
        else None
    )


def __number_or_range_pattern(valid_number_len: int) -> Any:
    return re.compile(
        r"^\[(\d{1,"
        + str(valid_number_len)
        + r"})\s+TO\s+(\d{1,"
        + str(valid_number_len)
        + r"})]|(\d{1,"
        + str(valid_number_len)
        + r"})$"
    )


def __all_values_in_range(match: Any, smallest: int, largest: int) -> bool:
    count_invalid = reduce(
        lambda acc, x: acc + 1
        if x is not None and (int(x) < smallest or int(x) > largest)
        else acc,
        match.groups(),
        0,
    )

    return count_invalid == 0
