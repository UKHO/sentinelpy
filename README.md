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
</p>
</details>



## `QuerySentinelProductsResponse`

# Features

* Queries the Sentinel Hub for products

# Credits

This package was created with Cookiecutter and the `UKHO/cookiecutter-pypackage` project template.

* Cookiecutter: https://github.com/cookiecutter/cookiecutter
* UKHO/cookiecutter-pypackage: https://github.com/UKHO/cookiecutter-pypackage
