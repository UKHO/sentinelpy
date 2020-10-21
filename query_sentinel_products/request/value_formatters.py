import re
from typing import Union

__NO_BRACKETS_NUMERIC_RANGE_PATTERN = re.compile(r"^\d+\sTO\s\d+$")


def format_footprint(footprint: str) -> str:
    """Formats the supplied footprint so that it conforms to the Sentinel format
    i.e. using Intersects and quotations

    Args:
          footprint::str
            AOI Footprint which may be a Coordinate Pair, WKT Polygon bounding box or
            Intersects fn call
    Returns:
          val::str
            Formatted footprint compatible with Sentinel Hub API
    """
    intersects_pattern = re.compile(r"^\"?Intersects\((.+)\)\"?$")
    intersects_match = intersects_pattern.match(footprint)
    return (
        f'"Intersects({footprint})"'
        if intersects_match is None
        else f'"Intersects({intersects_match.group(1)})"'
    )


def format_number_or_range(orbit_number: Union[str, int]) -> str:
    """Formats the supplied orbit number so that it is compatible with Sentinel API
    if the range does not have braces around it then this will be supplied.

    Args:
        orbit_number::Union[str, int]
            Orbit number that may be integer, string range

    Returns:
        val::str
            If int supplied just returns the value as string otherwise if it is a group
            appends the brackets around so that it is compatible with Sentinel Hub API
    """

    return (
        str(orbit_number)
        if __NO_BRACKETS_NUMERIC_RANGE_PATTERN.match(str(orbit_number)) is None
        else f"[{orbit_number}]"
    )
