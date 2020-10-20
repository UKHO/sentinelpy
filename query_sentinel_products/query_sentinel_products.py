"""Main module."""
from collections import namedtuple

import requests

from .request.model import SentinelProductRequest

SentinelProductResponse = namedtuple(
    "SentinelProductResponse", ["status_code", "body", "error"]
)
SENTINEL_HUB_URL_PATTERN = (
    "https://scihub.copernicus.eu/dhus/search?q={query}"
    "&rows={rows}&start={start}{additional_params}&format=json"
)


def query_sentinel_hub(
    sentinel_product_request: SentinelProductRequest,
) -> SentinelProductResponse:
    requests.get(
        __build_url(sentinel_product_request),
        auth=(sentinel_product_request.username, sentinel_product_request.password),
    )
    return SentinelProductResponse(None, None, None)


def __build_url(sentinel_product_request: SentinelProductRequest) -> str:
    additional_params = (
        ""
        if sentinel_product_request.order_by is None
        else f"&orderby={sentinel_product_request.order_by}"
    )
    return SENTINEL_HUB_URL_PATTERN.format(
        query=sentinel_product_request.query,
        rows=sentinel_product_request.rows,
        start=sentinel_product_request.start,
        additional_params=additional_params,
    )
