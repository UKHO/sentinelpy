from typing import AnyStr, Dict, List
from urllib.parse import parse_qs


def get_query_parameters_of_url(url: str) -> Dict[str, List[AnyStr]]:
    just_query_params = url[url.index("?") + 1 :]
    return parse_qs(just_query_params)
