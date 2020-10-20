# query_sentinel_products

![Python Package](https://github.com/UKHO/query_sentinel_products/workflows/Python%20package/badge.svg)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=UKHO/query_sentinel_products&identifier=304287716)](https://dependabot.com)

Queries ESA Sentinel APIs for products


* Free software: MIT license

# Usage
Import `query_sentinel_hub`.

<details>
<summary><strong>query_sentinel_hub</strong></summary>

<p>

**Positional arguments:**

* `sentinel_product_request` (_SentinelProductRequest_)

    Request object containing the details of the query. You can use the builder to
    construct

**Keyword arguments:**

* `log_level` (_int_)

    Level for which to log at use `logging` to define correct level

**Returns:** [_QuerySentinelProductsResponse_](#QuerySentinelProductsResponse) object
</p>
</details>

<details id="QuerySentinelProductsResponse">
<summary><strong>QuerySentinelProductsResponse</strong></summary>

<p>

Represents the result from the Sentinel Hub API

Can be interacted with as an object or in a more functional style using
the 'on' methods.

#### Properties

* `status_code` (_Optional[int]_)

    The HTTP Status code representing the outcome of the query

* `data` (_Optional[Dict[str, Any]]_)

    The resulting data from the Sentinel Hub

* `error` (_Optional[BaseException]_)

    An error object if there was an error or exception raised

* `success` (_bool_)

    Whether or not the query was successful

* `tuple` (QuerySentinelProductsResponseTuple)

    Converts the result into a named tuple so that it can be
    easily consumed.

#### Methods

<details>
<summary>Method detail</summary>

<p>

##### `raise_error`

If encountered an error raise so not

Situations this would be useful:

- Prevent exceptions being swallowed
- You prefer to handle exception rather than checking if value is None

**Returns**: _None_

**Raises**: Error that was encountered when querying the API
</p>
</details>
</p>
</details>



## `QuerySentinelProductsResponse`

# Features

* Queries the Sentinel Hub for products

# Credits

This package was created with Cookiecutter and the `UKHO/cookiecutter-pypackage` project template.

* Cookiecutter: https://github.com/cookiecutter/cookiecutter
* UKHO/cookiecutter-pypackage: https://github.com/UKHO/cookiecutter-pypackage
