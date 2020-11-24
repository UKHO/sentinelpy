"""Main module."""
import logging
from typing import Optional
from urllib.parse import urlencode

import requests

from .exceptions import QuerySentinelProductsError
from .query_sentinel_products_response import QuerySentinelProductsResponse
from .request.model import SentinelProductRequest

__SENTINEL_HUB_URL_PATTERN = "https://scihub.copernicus.eu/dhus/search?{query}"


def query_sentinel_hub(
    sentinel_product_request: SentinelProductRequest,
    *,
    log_level: int = logging.INFO,
    logger: Optional[logging.Logger] = None,
) -> QuerySentinelProductsResponse:
    """Queries the Sentinel Hub for the information in the request.

    Args:
        sentinel_product_request::SentinelProductRequest
            Details regarding the request

        log_level::int
            Level of logs to print

        logger::Optional[logging.Logger]
            Logger to log information and error message defaults to None

    Returns:
        result::QuerySentinelProductsResponse
            Result of the query
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    try:
        response = __call_api(sentinel_product_request, logger)
        logger.info(
            f"Received response from Sentinel hub with status: {response.status_code}"
        )
        return __read_response(response)
    except IOError as request_exception:
        return QuerySentinelProductsResponse(None, None, request_exception)


def __call_api(
    sentinel_product_request: SentinelProductRequest, logger: logging.Logger
) -> requests.Response:
    logger.debug(f"Querying sentinel hub with request: {sentinel_product_request}")
    url = __build_url(sentinel_product_request)
    auth = (sentinel_product_request.username, sentinel_product_request.password)
    logger.debug(f"Constructed url: {url}")
    return requests.get(url, auth=auth,)


def __read_response(response: requests.Response) -> QuerySentinelProductsResponse:
    try:
        data = response.json()
        return QuerySentinelProductsResponse(response.status_code, data)
    except ValueError as json_error:
        return QuerySentinelProductsResponse(
            response.status_code,
            None,
            QuerySentinelProductsError(
                json_error, response.status_code, response.content.decode()
            ),
        )


def __build_url(sentinel_product_request: SentinelProductRequest) -> str:
    query_params = {
        "q": sentinel_product_request.query,
        "start": sentinel_product_request.start,
        "format": "json",
    }

    if sentinel_product_request.rows is not None:
        query_params["rows"] = sentinel_product_request.rows

    if sentinel_product_request.order_by is not None:
        query_params["orderby"] = sentinel_product_request.order_by

    return __SENTINEL_HUB_URL_PATTERN.format(query=urlencode(query_params))
