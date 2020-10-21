from typing import Any, Callable, Dict, NamedTuple, Optional


class QuerySentinelProductsResponse(NamedTuple):
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
    ).on_failure(
        lambda tuple, data: print(f'failure:{tuple[0]}')
    ) # success:{}

    """

    status_code: Optional[int]
    body: Optional[Dict[str, Any]]
    error: Optional[BaseException] = None

    @property
    def success(self) -> bool:
        return (
            self.error is None
            and self.status_code is not None
            and 200 <= self.status_code < 300
        )

    def raise_error(self):
        """If encountered an error raise so not

        Situations this would be useful:
        - Prevent exceptions being swallowed
        - You prefer to handle exception rather than checking if value is None
        """
        if self.error is not None:
            raise self.error

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
        if self.body is not None and self.success:
            callback(self.body)
        return self

    def on_failure(
        self, callback: Callable[["QuerySentinelProductsResponse"], None],
    ) -> "QuerySentinelProductsResponse":
        """Calls callback if the request failed in some way either could not
        reach API or there was an error in the response or parsing the response

        Args:
            callback::Callable["QuerySentinelProductsResponse"]
                Callback to call if was failure.

        Returns:
            self::QuerySentinelProductsResponse
        """
        if not self.success or self.body is None:
            callback(self)
        return self
