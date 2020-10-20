"""Main module."""
import logging

import requests

from .exceptions import QuerySentinelProductsError
from .query_sentinel_products_response import QuerySentinelProductsResponse
from .request.model import SentinelProductRequest

__SENTINEL_HUB_URL_PATTERN = (
    "https://scihub.copernicus.eu/dhus/search?q={query}"
    "&rows={rows}&start={start}{additional_params}&format=json"
)


def query_sentinel_hub(
    sentinel_product_request: SentinelProductRequest, *, log_level: int = logging.INFO
) -> QuerySentinelProductsResponse:
    logger = logging.getLogger()
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
    additional_params = (
        ""
        if sentinel_product_request.order_by is None
        else f"&orderby={sentinel_product_request.order_by}"
    )
    return __SENTINEL_HUB_URL_PATTERN.format(
        query=sentinel_product_request.query,
        rows=sentinel_product_request.rows,
        start=sentinel_product_request.start,
        additional_params=additional_params,
    )