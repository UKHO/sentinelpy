import re
from typing import Callable, List, Optional, Union

from .model import (
    FilterKeyword,
    OrbitDirection,
    PlatformName,
    PolarisationMode,
    ProductType,
    SensorOperationalMode,
    SwathIdentifier,
    Timeliness,
)
from .validate_query_builder_args import (
    cloud_coverage_percentage_validator,
    date_value_validator,
    geometry_type_validator,
    orbit_number_validator,
    relative_orbit_number_validator,
    string_not_empty_validator,
)
from .value_formatters import format_footprint, format_number_or_range


def range_value(start_val: str, end_value: str) -> str:
    """Helper function to create a Sentinel API compliant range for fields such
     as orbit_number etc."""
    return f"[{start_val} TO {end_value}]"


class RequestQueryBuilder:
    """ Builder class for creating Queries of Sentinel data

    Reference:
    https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch
    for complete manual of querying the Sentinel hub, each search keyword
    maps to a method on the builder.

    Examples
    ========

    q = RequestQueryBuilder().platform_name(PlatformName.SENTINEL_1).build()
    # equivalent of `q=platformname:Sentinel-1`

    q = (
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
    # q = 'platformname:Sentinel-3 AND cloudcoverpercentage:[0 TO 5] AND \
    # footprint:"Intersect(POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.80,-4.53 46.80,\
    # -4.53 29.85)))"'

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
    # q = "(platformname:Sentinel-1 AND polarisationmode:HH) OR \
    # (platformname:Sentinel-1 AND NOT polarisationmode:VH)"
    """

    def __init__(self):
        self.__filters: List[str] = []

    def and_(self) -> "RequestQueryBuilder":
        """Logical and
        """
        self.__filters += ["AND"]
        return self

    def or_(self) -> "RequestQueryBuilder":
        """Logical or
        """
        self.__filters += ["OR"]
        return self

    def not_(self) -> "RequestQueryBuilder":
        """Logical NOT
        """
        self.__filters += ["NOT"]
        return self

    def group_(
        self, inner_query: Union["RequestQueryBuilder", str]
    ) -> "RequestQueryBuilder":
        """Create a group in the query.

        Args:
            inner_query: Union[RequestQueryBuilder, str])
                The content for the inner query - if a builder calls build
        """
        group_query = (
            inner_query if isinstance(inner_query, str) else inner_query.build()
        )
        self.__filters += [f"({group_query})"]
        return self

    def platform_name(self, platform_name: PlatformName) -> "RequestQueryBuilder":
        """Filter on platform name
        """
        self.__add_filter(FilterKeyword.PLATFORM_NAME, platform_name.value)
        return self

    def begin_position(
        self, begin_position_start: str, begin_position_end: str
    ) -> "RequestQueryBuilder":
        """Filter on beginposition

        Args:
            begin_position_start::str
                Start of the period, in ISO date/time stamp with millis, or relative
                to NOW (e.g. NOW/NOW-1DAY etc.)
            begin_position_end::str
                End of the period, in ISO date/time stamp with millis, or relative
                to NOW (e.g. NOW/NOW-1DAY etc.)

        Raises:
            ValueError - if begin_position_start or begin_position_end are invalid
            ISO dates/relative dates
        """

        return self.__add_range_keyword_filter(
            FilterKeyword.BEGIN_POSITION,
            begin_position_start,
            begin_position_end,
            date_value_validator,
            lambda: (
                "begin_position_start and begin_position_end need to be a full ISO "
                "date or timestamp relative to now"
            ),
        )

    def end_position(
        self, end_position_start: str, end_position_end: str
    ) -> "RequestQueryBuilder":
        """Set a filter on the range for endposition (that is Sensing Stop Time)
        that the query is interested in.

        Args:
            end_position_start::str
                Start of the period, in ISO date/time stamp with millis, or relative to
                NOW (e.g. NOW/NOW-1DAY etc.)
            end_position_end::str
                End of the period, in ISO date/time stamp with millis, or relative to
                NOW (e.g. NOW/NOW-1DAY etc.)

         Raises:
            ValueError - if end_position_start or end_position_end are invalid ISO
            dates/relative dates
        """
        return self.__add_range_keyword_filter(
            FilterKeyword.END_POSITION,
            end_position_start,
            end_position_end,
            date_value_validator,
            lambda: (
                "end_position_start and end_position_end need to be a full ISO "
                "date or timestamp relative to now"
            ),
        )

    def ingestion_date(
        self, ingestion_date_start: str, ingestion_date_end: str
    ) -> "RequestQueryBuilder":
        """Sets a filter on the ingestion date using supplied range

        Args:
            ingestion_date_start::str
                Start of the period,  in ISO date/time stamp with millis, or relative
                to NOW (e.g. NOW/NOW-1DAY etc.)
            ingestion_date_end::str
                End of the period, in ISO date/time stamp with millis, or relative
                to NOW (e.g. NOW/NOW-1DAY etc.)

        Raises:
            ValueError - if end_position_start or end_position_end are invalid ISO
            dates/relative dates
        """
        return self.__add_range_keyword_filter(
            FilterKeyword.INGESTION_DATE,
            ingestion_date_start,
            ingestion_date_end,
            date_value_validator,
            lambda: (
                "ingestion_date_start and ingestion_date_end need to be a full ISO "
                "date or timestamp relative to now"
            ),
        )

    def collection(self, collection: str) -> "RequestQueryBuilder":
        """Sets a filter on the collection. Used to specify the name
        of a predefined collection of products

        Args:
            collection::str
                Name of the collection

        Raises:
            ValueError - If collection is blank - i.e. '' or just whitespace e.g. ' '
        """
        return self.__add_keyword_filter(
            FilterKeyword.COLLECTION,
            collection,
            string_not_empty_validator,
            lambda: "collection should not be empty",
        )

    def file_name(self, filename: str) -> "RequestQueryBuilder":
        """Sets a filter on product filename.

        Args:
            filename::str
                Name of the Sentinel image file to filter results by

        Raises:
            ValueError - If filename is blank - i.e. '' or just whitespace e.g. ' '
        """
        return self.__add_keyword_filter(
            FilterKeyword.FILE_NAME,
            filename,
            string_not_empty_validator,
            lambda: "filename should not be empty",
        )

    def footprint(self, geographic_type: str) -> "RequestQueryBuilder":
        """Sets a filter on geographic area that the query is interested in. Can use
        either a simple bounding box described as a WKT Polygon or a point described
        by a `Latitude` `Longitude` pair. Refer to the Sentinel Hub documentation for
        in depth information about footprint.

        Args:
              geographic_type::str
                The Area of Interest for the query. Can either be a point (lat/lon
                pair e.g. "0.000, 1.000") or a Polygon (WKT polygon without cut outs,
                e.g. POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10)))

                Can have the Intersects() or can be just the coordinate pair or Polygon

        Raises:
            ValueError - If supplied geographic type is not supported Geographic format
            i.e. long/lat pair or WKT polygon
        """
        return self.__add_keyword_filter(
            FilterKeyword.FOOTPRINT,
            format_footprint(geographic_type),
            geometry_type_validator,
            lambda: "footprint must be called with valid geometry type - coordinate "
            "pair or simple polygon",
        )

    def orbit_number(self, orbit_number: Union[int, str]) -> "RequestQueryBuilder":
        """Adds a filter on orbitnumber

        Args:
            orbit_number::Union[int, str]
                The orbit number or range that should be used. Can be a single value
                i.e. 1234 or a range such as [1234 TO 4321]

        Raises:
            ValueError - If orbit_number is not a single value of range (1-999999)
        """
        return self.__add_keyword_filter(
            FilterKeyword.ORBIT_NUMBER,
            format_number_or_range(orbit_number),
            orbit_number_validator,
            lambda: (
                "orbitnumber must be a range or single numeric value between "
                "1 and 999999"
            ),
        )

    def last_orbit_number(self, orbit_number: Union[int, str]) -> "RequestQueryBuilder":
        """Adds a filter for lastorbitnumber

        Args:
            orbit_number::Union[int, str]
                The orbit number or range that should be used. Can be a single value
                i.e. 1234 or a range such as [1234 TO 4321]

        Raises:
            ValueError - If orbit_number is not a single value of range (1-999999)
        """
        return self.__add_keyword_filter(
            FilterKeyword.LAST_ORBIT_NUMBER,
            format_number_or_range(orbit_number),
            orbit_number_validator,
            lambda: (
                "lastorbitnumber must be a range or single numeric value between "
                "1 and 999999"
            ),
        )

    def relative_orbit_number(
        self, orbit_number: Union[int, str]
    ) -> "RequestQueryBuilder":
        """Sets query for relative orbit number

        Args:
            orbit_number::Union[int, str]
                The orbit number or range that should be used. Can be a single value
                i.e. 20 or a range such as [1 TO 170]

        Raises:
            ValueError - If orbit_number is not a single value of range (1-175)
        """
        return self.__add_keyword_filter(
            FilterKeyword.RELATIVE_ORBIT_NUMBER,
            format_number_or_range(orbit_number),
            relative_orbit_number_validator,
            lambda: (
                "relativeorbitnumber must be a range or single numeric value between "
                "1 and 175"
            ),
        )

    def last_relative_orbit_number(
        self, orbit_number: Union[int, str]
    ) -> "RequestQueryBuilder":
        """Sets a filter on the last orbit number or range range of last orbit
        numbers (i.e `[MIN TO MAX]` whereby MIN is the lowest last orbit number
        and MAX is highest). Relative orbit number of the oldest line within the image
        data (the start of the product) and relative orbit number of the most recent
        line within the image data (the end of the product), respectively.

        Args:
            orbit_number::Union[int, str]
                The orbit number or range that should be used. Can be a single value
                i.e. 20 or a range such as [1 TO 170]

        Raises:
            ValueError - If orbit_number is not a single value of range (1-175)
        """
        return self.__add_keyword_filter(
            FilterKeyword.LAST_RELATIVE_ORBIT_NUMBER,
            format_number_or_range(orbit_number),
            relative_orbit_number_validator,
            lambda: (
                "lastrelativeorbitnumber must be a range or single numeric value "
                "between 1 and 175"
            ),
        )

    def orbit_direction(self, orbit_direction: OrbitDirection) -> "RequestQueryBuilder":
        """Sets a filter on the orbit direction for the oldest data in the product"""
        self.__add_filter(FilterKeyword.ORBIT_DIRECTION, orbit_direction.value)
        return self

    def polarisation_mode(
        self, polarisation_mode: PolarisationMode
    ) -> "RequestQueryBuilder":
        """Set filter on polarisation mode"""
        self.__add_filter(FilterKeyword.POLARISATION_MODE, polarisation_mode.value)
        return self

    def product_type(self, product_type: ProductType) -> "RequestQueryBuilder":
        """Set filter on product type"""
        self.__add_filter(FilterKeyword.PRODUCT_TYPE, product_type.value)
        return self

    def sensor_operational_mode(self, sensor_operational_mode: SensorOperationalMode):
        """Set filter on sensor operational mode"""
        self.__add_filter(
            FilterKeyword.SENSOR_OPERATIONAL_MODE, sensor_operational_mode.value
        )
        return self

    def swath_identifier(
        self, swath_identifier: SwathIdentifier
    ) -> "RequestQueryBuilder":
        """Set filter on swath identifier"""
        self.__add_filter(FilterKeyword.SWATH_IDENTIFIER, swath_identifier.value)
        return self

    def cloud_cover_percentage(
        self, percentage: Union[int, str]
    ) -> "RequestQueryBuilder":
        """Sets a filter on cloud cover percentage.

        Args:
            percentage::Union[int, str]
                Acceptable limits of cloud cover. Can be an int between 0 and 100, or
                a range with the same limits

        Raises:
            ValueError - if percentage is not a valid integral percentage
        """
        return self.__add_keyword_filter(
            FilterKeyword.CLOUD_COVER_PERCENTAGE,
            format_number_or_range(percentage),
            cloud_coverage_percentage_validator,
            lambda: (
                "cloudcoverpercentage must be valid integral percentage number or "
                "range between 0 and 100"
            ),
        )

    def timeliness(self, timeliness: Timeliness) -> "RequestQueryBuilder":
        """Set filter on timeliness"""
        self.__add_filter(FilterKeyword.TIMELINESS, timeliness.value)
        return self

    def build(self) -> str:
        """Build the value for 'q'"""
        query = ""
        prev_filter = ""
        for curr_filter in self.__filters:
            if (
                prev_filter != ""
                and not RequestQueryBuilder.__is_operator(curr_filter)
                and not RequestQueryBuilder.__is_operator(prev_filter)
            ):
                query += "AND "
            query += f"{curr_filter} "
            prev_filter = curr_filter

        return (
            RequestQueryBuilder.__strip_dangling_operator_and_whitespace(query)
            if query != ""
            else "*"
        )

    def __add_range_keyword_filter(
        self,
        keyword: FilterKeyword,
        start: str,
        end: str,
        validator: Callable[[str], Optional[str]],
        invalid_msg_cb: Callable[[], str],
    ) -> "RequestQueryBuilder":
        valid_start = validator(start)
        valid_end = validator(end)

        if valid_start and valid_end:
            self.__add_filter(keyword, range_value(valid_start, valid_end))
            return self
        else:
            raise ValueError(invalid_msg_cb())

    def __add_keyword_filter(
        self,
        keyword: FilterKeyword,
        val: str,
        validator: Callable[[str], Optional[str]],
        invalid_msg_cb: Callable[[], str],
    ) -> "RequestQueryBuilder":
        valid_value = validator(val)

        if valid_value:
            self.__add_filter(keyword, valid_value)
            return self
        else:
            raise ValueError(invalid_msg_cb())

    def __add_filter(self, keyword: FilterKeyword, value: str):
        self.__filters += [f"{keyword.value}:{value}"]

    @staticmethod
    def __is_operator(filter_val: str):
        return filter_val in ["AND", "OR", "NOT"]

    @staticmethod
    def __strip_dangling_operator_and_whitespace(query):
        hanging_operator_pattern = re.compile(r"^(?:AND|OR)\s*|\s*(?:AND|OR|NOT)?\s*$")
        return hanging_operator_pattern.sub("", query)
