from collections import namedtuple
from typing import Any, Callable, Dict, Optional

QuerySentinelProductsResponseTuple = namedtuple(
    "SentinelProductResponse", ["status_code", "body", "error"]
)


class QuerySentinelProductsResponse:
    """Represents the result from the Sentinel Hub API

    Can be interacted with as an object or in a more functional style using
    the 'on' methods.

    Examples
    ========
    # Successful response:
    successful_response = QuerySentinelProductsResponse(200, {})
    print(successful_response.success) # True
    print(successful_response.status_code) # 200
    print(successful_response.data) # {}
    print(successful_response.error) # None

    # Failed response:
    failed_response = QuerySentinelProductsResponse(400, {})
    print(failed_response.success) # False
    print(failed_response.status_code) # 400
    print(failed_response.data) # {}
    print(failed_response.error) # None

    # Erroneous response
    erroneous_response = QuerySentinelProductsResponse(None, None, IOError)
    print(erroneous_response.success) # False
    print(erroneous_response.status_code) # None
    print(erroneous_response.data) # None
    print(erroneous_response.error) # IOError

    # Using the functional style methods
    successful_response.on_success(
        lambda data: print(f'success:{data}')
    ).on_error(
        lambda error: print(f'error:{error}')
    ).on_failure(
        lambda status_code, data: print(f'failure:{status_code}')
    ) # success:{}

    """

    def __init__(
        self,
        status_code: Optional[int],
        data: Optional[Dict[str, Any]],
        error: Optional[BaseException] = None,
    ):
        self.__status_code = status_code
        self.__data = data
        self.__error = error

    @property
    def status_code(self) -> Optional[int]:
        return self.__status_code

    @property
    def data(self) -> Optional[Dict[str, Any]]:
        return self.__data

    @property
    def error(self) -> Optional[BaseException]:
        return self.__error

    @property
    def success(self) -> bool:
        return (
            self.__error is None
            and self.__status_code is not None
            and 200 <= self.__status_code < 300
        )

    @property
    def tuple(self):
        """Converts the result into a named tuple so that it can be
        easily consumed."""
        return QuerySentinelProductsResponseTuple(
            self.__status_code, self.__data, self.__error
        )

    def raise_error(self):
        """If encountered an error raise so not

        Situations this would be useful:
        - Prevent exceptions being swallowed
        - You prefer to handle exception rather than checking if value is None
        """
        if self.__error is not None:
            raise self.__error

    def on_success(
        self, callback: Callable[[Dict[str, Any]], None]
    ) -> "QuerySentinelProductsResponse":
        """Calls supplied callback with data if the api call was successful

        Args:
            callback::Callable[[BaseException], None]
                Callback to call if was success

        Returns:
            self::QuerySentinelProductsResponse
        """
        if self.__data is not None and self.success:
            callback(self.__data)
        return self

    def on_error(
        self, callback: Callable[[BaseException], None]
    ) -> "QuerySentinelProductsResponse":
        """Calls supplied callback with exception if there was an error raised

        Args:
            callback::Callable[[BaseException], None]
                Callback to call when there is an error

        Returns:
            self::QuerySentinelProductsResponse
        """
        if self.__error is not None:
            callback(self.__error)
        return self

    def on_failure(self, callback: Callable[[int, Dict[str, Any]], None]):
        """Calls callback if API call failed because the API call failed
        because a non-2XX response code was received

        Args:
            callback::Callable[[int, Dict[str, Any]], None]
                Callback to call if was failure.

        Returns:
            self::QuerySentinelProductsResponse
        """
        if (
            self.__status_code is not None
            and self.__status_code >= 300
            and self.__error is None
        ):
            callback(self.__status_code, self.__data if self.__data is not None else {})
        return self

    def __eq__(self, o: object) -> bool:
        return isinstance(o, QuerySentinelProductsResponse) and o.tuple == self.tuple
