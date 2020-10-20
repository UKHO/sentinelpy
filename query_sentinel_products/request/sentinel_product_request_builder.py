from __future__ import annotations

from typing import Optional, Union

from .model import SentinelProductRequest
from .request_query_builder import RequestQueryBuilder


class SentinelProductRequestBuilder:
    """ Builder class to build Sentinel Product Requests
    """

    __username: Optional[str]
    __password: Optional[str]
    __query: Union[RequestQueryBuilder, str]

    def __init__(
        self,
        default_query: str = "*",
        default_rows: int = 30,
        default_order_by: Optional[str] = None,
        default_start: int = 0,
    ):
        self.__username = None
        self.__password = None
        self.__query = default_query
        self.__rows = default_rows
        self.__order_by = default_order_by
        self.__start = default_start

    def with_username(self, username: str) -> "SentinelProductRequestBuilder":
        """ Sets the Sentinel Hub username

        Args:
            username::str
                The username for the Sentinel Hub API
        Returns:
            self::SentinelProductRequestBuilder
                Builder with username set
        """
        self.__username = username
        return self

    def with_password(self, password: str) -> "SentinelProductRequestBuilder":
        """ Sets the Sentinel Hub password

        Args:
            password::str
                The password for the Sentinel Hub API
        Returns:
            self::SentinelProductRequestBuilder
                Builder with password set
        """
        self.__password = password
        return self

    def with_query(
        self, query: Union[str, RequestQueryBuilder]
    ) -> "SentinelProductRequestBuilder":
        """ Sets the query value
        Args:
            query::[Union[str, RequestQueryBuilder]]
                The query that the request performs. If it is a RequestQueryBuilder,
                build calls build before returning the SentinelProductRequest
        Returns:
            self::SentinelProductRequestBuilder
                Builder with query set
        """
        self.__query = query
        return self

    def with_rows(self, rows: int) -> "SentinelProductRequestBuilder":
        """ Sets the rows value
        Args:
            rows::int
                Number of rows to return in each request
        Returns:
            self::SentinelProductRequestBuilder
                Builder with rows set
        """
        self.__rows = rows
        return self

    def with_ordering(self, order_by: str) -> "SentinelProductRequestBuilder":
        """ Sets the ordering/order_by value
        Args:
            order_by::str
                Field to sort the results by and order of the sort e.g.
                'beginposition desc'
        Returns:
            self::SentinelProductRequestBuilder
                Builder with ordering set
        """
        self.__order_by = order_by
        return self

    def with_start(self, start: int) -> "SentinelProductRequestBuilder":
        """ Sets the start number/offset. Used for paginating results
        Args:
            start::int
                Start index to retrieve, not required
        Returns:
            self::SentinelProductRequestBuilder
                Builder with start set
        """
        self.__start = start
        return self

    def build(self) -> SentinelProductRequest:
        """
        Returns:
            request::SentinelProductRequest
                Request with the values that have been provided to the builder

        Side Effects:
            ValueError - Username or Password not supplied
        """
        self.__assert_mandatory_fields_present()
        query = (
            self.__query
            if not isinstance(self.__query, RequestQueryBuilder)
            else self.__query.build()
        )
        rows = self.__rows
        order_by = self.__order_by
        start = self.__start
        username = self.__username
        password = self.__password
        return SentinelProductRequest(
            query=query,
            rows=rows,
            order_by=order_by,
            start=start,
            username=username,
            password=password,
        )

    def __assert_mandatory_fields_present(self):
        errors = ""
        if self.__username is None:
            errors = "username is required; "
        if self.__password is None:
            errors += "password is required; "

        if errors:
            raise ValueError(errors.strip())
