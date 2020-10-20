from typing import Optional


class QuerySentinelProductsError(BaseException):
    def __init__(
        self, source: BaseException, status_code: Optional[int], response_data: str
    ):
        self.source = source
        self.status_code = status_code
        self.response_data = response_data

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, QuerySentinelProductsError)
            and o.response_data == self.response_data
            and o.status_code == self.status_code
            and o.source == self.source
        )
