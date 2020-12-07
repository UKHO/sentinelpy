# sentinelpy

![Python Package](https://github.com/UKHO/sentinelpy/workflows/Python%20Package/badge.svg?branch=main)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=UKHO/sentinelpy&identifier=304287716)](https://dependabot.com)

Queries ESA Sentinel APIs for products


* Free software: MIT license

# Usage
## `query_sentinel_hub`

```python
import logging

from sentinelpy import (
    query_sentinel_hub,
    SentinelProductRequestBuilder,
    RequestQueryBuilder,
    PlatformName,
    QuerySentinelProductsResponse
)

request = (
    SentinelProductRequestBuilder()
    .with_username("username")
    .with_password("password")
    .with_query(
        RequestQueryBuilder()
        .platform_name(PlatformName.SENTINEL_1)
    )
    .build()
)

result = query_sentinel_hub(request, log_level=logging.DEBUG)

assert isinstance(result, QuerySentinelProductsResponse)

print(result.status_code)
print(result.body)
print(result.error)
```

**Positional arguments:**

* `sentinel_product_request` (_[SentinelProductRequest](#SentinelProductRequest)_)

    Request object containing the details of the query. You should use the _[SentinelProductRequestBuilder](#SentinelProductRequestBuilder)_ to
    construct

**Keyword arguments:**

* `log_level` (_int_)

    Level for which to log at use `logging` to define correct level, defaults to 'INFO'.

* `logger` (_logging.Logger_)

    Logger to use to log messages with, defaults to `logging.getLogger(__name__)` if no value supplied

**Returns:** _[QuerySentinelProductsResponse](#QuerySentinelProductsResponse)_ object

## API Documentation
<details>
<summary><strong>range_value</strong></summary>

<p>

### range_value (`function`)

A helper function for defining range values for queries using the `RequestQueryBuilder`

**Parameters**:

* `start_val` (_str_)

    Start of the range
* `end_val` (_str_)

    End of the range

**Returns**: _str_ range string in format of "[MIN TO MAX]" where `MIN` is `start_val` and `MAX` is `end_val`

#### Example

```python
from sentinelpy import (
    RequestQueryBuilder,
    range_value
)

query = (
    RequestQueryBuilder()
    .orbit_number(range_value("1", "2"))
    .build()
)

assert query == "orbitnumber:[1 TO 2]"
```
</p>
</details>

---

<details id="SentinelProductRequestBuilder">
<summary><strong>SentinelProductRequestBuilder</strong></summary>

<p>

### SentinelProductRequestBuilder (`class`)
Builder resposible for creating _[SentinelProductRequest](#SentinelProductRequest)_ objects.

As a minimum, the username and password for the Sentinel Hub should be supplied.

<details>
<summary><strong>Constructor details</strong></summary>

<p>

* **`default_query`** (_str_): Default value for query, _defaults to `*`_
* **`default_rows`** (_int_): Default value for rows, _defaults to `30`_
* **`default_order_by`** (_Optional[str]_): Default value for order by, _defaults to `None`_
* **`default_start`** (_int_): Default value for start, _defaults to `0`_
</p>
</details>

<details>
<summary><strong>Method details</strong></summary>

<p>

##### `build`

Method that constructs the _[SentinelProductRequest](#SentinelProductRequest)_ using the values supplied to the builder

**Returns**: _`SentinelProductRequest`_ - Built request from input data

**Raises**: _`ValueError`_ - if username or password missing

---

##### `with_username`

Sets the Sentinel Hub username

**Parameter**:

* `username` (_str_)

    The username for Sentinel Hub API

**Returns**: _SentinelProductRequestBuilder_ Builder object with `username` supplied

---

##### `with_password`

Sets the Sentinel Hub password

**Parameter**:

* `password` (_str_)

    The associated password for the user for the Sentinel Hub API

**Returns**: _SentinelProductRequestBuilder_ Builder object with `password` supplied

---

##### `with_query`

Sets the query (q) value

**Parameter**:

* `query` (_str_ or _RequestQueryBuilder_)

    The query to use to filter results. If it is a _RequestQueryBuilder_, then `build` will
    call `build` on the _RequestQueryBuilder_ before constructing the _[SentinelProductRequest](#SentinelProductRequest)_.

**Returns**: _SentinelProductRequestBuilder_ Builder object with `query` supplied

---

##### `with_rows`

Sets the rows value

**Parameter**:

* `rows` (_int_)

    The value for rows to return in each request

**Returns**: _SentinelProductRequestBuilder_ Builder object with `rows` supplied

---

##### `with_order_by`

Sets the order_by value

**Parameter**:

* `order_by` (_str_)

    The value for order_by to return in each request

**Returns**: _SentinelProductRequestBuilder_ Builder object with `order_by` supplied

---

##### `with_start`

Sets the start value

**Parameter**:

* `start` (_int_)

    The value for start to return in each request

**Returns**: _SentinelProductRequestBuilder_ Builder object with `start` supplied


</p>
</details>

<details>
<summary><strong>Example usage</strong></summary>

<p>

```python
from sentinelpy import (
    SentinelProductRequestBuilder,
    SentinelProductRequest,
    RequestQueryBuilder,
    PlatformName,
)

minimal = (
    SentinelProductRequestBuilder()
    .with_username("username")
    .with_password("password")
    .build()
)

assert minimal == SentinelProductRequest(
    query="*",
    rows=None,
    order_by=None,
    start=0,
    username="username",
    password="password"
)

full = (
    SentinelProductRequestBuilder()
    .with_username("username")
    .with_password("password")
    .with_query(
        RequestQueryBuilder()
        .platform_name(PlatformName.SENTINEL_1)
    )
    .with_start(15)
    .with_rows(15)
    .with_order_by('ingestiondate desc')
    .build()
)

assert full == SentinelProductRequest(
    query="platformname:Sentinel-1",
    rows=15,
    order_by='ingestiondate desc',
    start=15,
    username="username",
    password="password"
)
```
</p>
</details>

</p>
</details>

---

<details id="RequestQueryBuilder">
<summary><strong>RequestQueryBuilder</strong></summary>

<p>

### RequestQueryBuilder (`class`)
A builder utility to build values for queries. [Refer to the Sentinel Hub API documentation for more information about the values](https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch). The methods of this class
map to search keywords/operators described in the former documentation. The keywords use snake case rather than
all lowercase to adhere to Python conventions.

<details>
<summary><strong>Method details</strong></summary>

<p>

##### `build`

Creates the value for query/`q` using the supplied values. If two non-operators supplied in order without an operator (i.e. `and_`, `or_`, or `not_`)
defaults to `and_` operator.

If the query has `and_` or `or_` operators at the start or an operator at the end then these are removed from the query.

**Returns**: _str_  - the query constructed using the builder, if no methods called returns `*` by default

**Example**

```python
from sentinelpy import RequestQueryBuilder, PlatformName

default_build_behaviour = RequestQueryBuilder().build()

assert default_build_behaviour == "*"

hanging_operator_start = RequestQueryBuilder().and_().platform_name(PlatformName.SENTINEL_1).build()

assert hanging_operator_start == "platformname:Sentinel-1"

hanging_operator_end = RequestQueryBuilder().not_().platform_name(PlatformName.SENTINEL_1).and_().build()

assert hanging_operator_end == "NOT platformname:Sentinel-1"
```

---

##### `and_`

Logical `and` - combines the previous and next clauses i.e. `platform_name(X).and_().platform_name(Y)` results in
the query being `platformname:X AND platform_name:Y`

**Returns**: _RequestQueryBuilder_ self

---

##### `or_`

Logical `or` - either the previous or next clauses i.e. `platform_name(X).or_().platform_name(Y)` results in
the query being `platformname:X OR platform_name:Y`

**Returns**: _RequestQueryBuilder_ self

---

##### `not_`

Negates the following clause.

**Returns**: _RequestQueryBuilder_ self

---

##### `group_`

Creates a grouped clause in the query. If the parameter is a _RequestQueryBuilder_ then it calls the `build` method
before.

**Parameter**:

* `inner_query` (_str_ or _RequestQueryBuilder_)

    The query that is part of the group.

**Returns**: _RequestQueryBuilder_ self

**Example**

```python
from sentinelpy import (
    RequestQueryBuilder,
    PlatformName,
    PolarisationMode
)

q = (
    RequestQueryBuilder()
    .group_(
        RequestQueryBuilder()
        .platform_name(PlatformName.SENTINEL_1)
        .and_()
        .polarisation_mode(PolarisationMode.HH)
    )
    .or_()
    .group_(
        RequestQueryBuilder()
        .platform_name(PlatformName.SENTINEL_1)
        .and_()
        .not_()
        .polarisation_mode(PolarisationMode.VH)
    )
    .build()
)
assert q == (
    "(platformname:Sentinel-1 AND polarisationmode:HH) OR "
    "(platformname:Sentinel-1 AND NOT polarisationmode:VH)"
)
```

---

##### `begin_position`

Sets the beginposition filter between the parameters start/end

**Parameters**:

* `begin_position_start` (_str_)

    Start of the range that the query is interested in, in ISO date/time stamp with millis, or relative
    to NOW (e.g. NOW/NOW-1DAY etc.)

* `begin_position_end` (_str_)

    End of the range that the query is interested in, in ISO date/time stamp with millis, or relative
    to NOW (e.g. NOW/NOW-1DAY etc.)

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ - if `begin_position_start` or `begin_position_end` are not valid, i.e not ISO or relative
date

---

##### `cloud_cover_percentage`

The range of acceptable values for cloud cover percentage as per Sentinel Dataset

**Parameter**:

* `percentage` (_int_ or _string_)

    The percentage value or range (the format of `MIN TO MAX` where MIN is lowest acceptable and MAX is upper limit)
    of limit for Cloud Cover Percentage

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if the value is not an integer or valid percentage or range

---

##### `collection`

Set the value for collection. Used to specify the name of a predefined collection of products

**Parameter**:

* `collection` (_str_)

    Value for collection

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if supplied string is empty i.e. '' or just whitespace

---

##### `end_position`

Set a filter on the range for endposition (that is Sensing Stop Time) that the query is interested in.

**Parameter**:

* `end_position_start` (_str_)

    Start of the period, in ISO date/time stamp with millis, or relative to NOW (e.g. NOW/NOW-1DAY etc.)

* `end_position_end` (_str_)

    End of the period, in ISO date/time stamp with millis, or relative to NOW (e.g. NOW/NOW-1DAY etc.)

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ - if `end_position_start` or `end_position_end` are not valid, i.e not ISO or relative
date

---

##### `file_name`

Sets a filter on product filename.

**Parameter**:

* `filename` (_str_)

    Name of the product file to filter results by

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if supplied string is empty i.e. '' or just whitespace

---

##### `footprint`

Sets a filter on geographic area that the query is interested in. Can use either a simple bounding box described
as a WKT Polygon or a point described by a `Latitude` `Longitude` pair. Refer to the Sentinel Hub documentation for
in depth information about footprint.

**Parameter**:

* `geographic_type` (_str_)

    The Area of Interest for the query. Can either be a point (lat/lon
    pair e.g. "0.000, 1.000") or a Polygon (WKT polygon without cut outs,
    e.g. POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10)))

    Can have the Intersects() or can be just the coordinate pair or Polygon

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if not valid WKT Polygon or point

---

##### `ingestion_date`

Sets a filter on the date the Sentinel product was ingested using the supplied range.

**Parameter**:

* `ingestion_date_start` (_str_)

    Start of the period,  in ISO date/time stamp with millis, or relative to NOW (e.g. NOW/NOW-1DAY etc.)

* `ingestion_date_end` (_str_)

    End of the period, in ISO date/time stamp with millis, or relative to NOW (e.g. NOW/NOW-1DAY etc.)

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ - if `ingestion_date_start` or `ingestion_date_end` are not valid, i.e not ISO or relative

---

##### `last_orbit_number`

Sets on a filter on the last orbit number or range range of last orbit numbers (i.e `[MIN TO MAX]` whereby MIN
is the lowest last orbit number and MAX is highest).

**Parameter**:

* `orbit_number` (_str_ or _int_)

    The orbit number or range that should be used. Can be a single value i.e. 1234 or a range such as [1234 TO 4321]
    must be between 0 and 999999

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if value is not a valid number or range

---

##### `last_relative_orbit_number`

Sets a filter on the last orbit number or range range of last orbit numbers (i.e `[MIN TO MAX]` whereby MIN
is the lowest last orbit number and MAX is highest). Relative orbit number of the oldest line within the image
data (the start of the product) and relative orbit number of the most recent line within the image data
(the end of the product), respectively.

**Parameter**:

* `orbit_number` (_str_ or _int_)

    The orbit number or range that should be used. Can be a single value i.e. 1234 or a range such as [1234 TO 4321]
    must be between 0 and 175

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if value is not a valid number or range

---

##### `orbit_direction`

Sets a filter on the orbit direction for the oldest data in the product

**Parameter**:

* `orbit_direction` (_[OrbitDirection](#Enumerations)_)

    Direction that the query is interested in

**Returns**: _RequestQueryBuilder_ self

---

##### `orbit_number`

Sets a filter on the orbit number or range range of orbit numbers (i.e `[MIN TO MAX]` whereby MIN
is the lowest orbit number and MAX is highest).

**Parameter**:

* `orbit_number` (_str_ or _int_)

    The orbit number or range that should be used. Can be a single value i.e. 1234 or a range such as [1234 TO 4321].
    must be between 0 and 999999

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if value is not a valid number or range

---

##### `platform_name`

Sets a filter on the platform name

**Parameter**:

* `platform_name` (_[PlatformName](#Enumerations)_)

    The platform name to filter the results by

**Returns**: _RequestQueryBuilder_ self

---

##### `polarisation_mode`

Sets a filter on polarisation mode.

**Parameter**:

* `polarisation_mode` (_[PolarisationMode](#Enumerations)_)


    Specified value for polarisation_mode

**Returns**: _RequestQueryBuilder_ self

---

##### `product_type`

Sets a filter on product type. Note the valid combinations with `platform_name`

**Parameter**:

* `product_type` [(_`Sentinel1ProductType`_ or _`Sentinel2ProductType`_ or _`Sentinel3ProductType`_ or _`Sentinel5PProductType`_)](#Enumerations)

    Specified value for product type to filter the results on

**Returns**: _RequestQueryBuilder_ self

---

##### `relative_orbit_number`

Set filter on relative orbit number of the oldest line within the image data (the start of the product).

**Parameter**:

* `orbit_number` (_str_ or _int_)

    The orbit number or range that should be used. Can be a single value i.e. 123 or a range such as [123 TO 124].
    must be between 0 and 175

**Returns**: _RequestQueryBuilder_ self

**Raises**: _ValueError_ if value is not a valid number or range

---

##### `sensor_operational_mode`

Set filter on sensor operational mode

**Parameter**:

* `sensor_operational_mode` (_[SensorOperationalMode](#Enumerations)_)

    The value to filter products on

**Returns**: _RequestQueryBuilder_ self

---

##### `swath_identifier`

Search all valid swath identifiers for the Sentinel-1 SAR instrument. The S1-S6 swaths apply to SM products, the IW and IW1-3 swaths apply to IW products (IW is used for detected IW products where the 3 swaths are merged into one image), the EW and EW1-5 swaths apply to EW products (EW is used for detected EW products where the 5 swaths are merged into one image).

**Parameter**:

* `swath_identifier` (_[SwathIdentifier](#Enumerations)_)

    Swath Identifier to filter products with

**Returns**: _RequestQueryBuilder_ self

---

##### `timeliness`

Filter sentinel products on timeliness

**Parameter**:

* `timeliness` (_[Timeliness](#Enumerations)_)

    Value of timeliness that the query is interested in

**Returns**: _RequestQueryBuilder_ self
</p>
</details>

<details>
<summary><strong>Example</strong></summary>

<p>

```python
from sentinelpy import RequestQueryBuilder, PlatformName

simple_q = (
    RequestQueryBuilder()
    .platform_name(PlatformName.SENTINEL_1)
    .build()
)

assert simple_q == "platformname:Sentinel-1"

multiple_clauses_q = (
    RequestQueryBuilder()
        .platform_name(PlatformName.SENTINEL_3)
        .and_()
        .cloud_cover_percentage("[0 TO 5]")
        .and_()
        .footprint(
            "POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.80,-4.53 46.80,-4.53 29.85))"
        )
        .build()
)

assert multiple_clauses_q == (
    'platformname:Sentinel-3 AND cloudcoverpercentage:[0 TO 5] AND '
    'footprint:"Intersects(POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.'
    '80,-4.53 46.80,-4.53 29.85)))"'
)
```
</p>
</details>
</p>
</details>

---

<details id="SentinelProductRequest">
<summary><strong>SentinelProductRequest</strong></summary>

<p>

### SentinelProductRequest (`NamedTuple`/`class`)

Named Tuple representing a request. Best practice would be to use the builders (_[SentinelProductRequestBuilder](#SentinelProductRequestBuilder)_ and _[RequestQueryBuilder](#RequestQueryBuilder)_) to derive.

#### Properties:

* `query` (_str_)

    Query string value for 'q' in the request. [Sentinel hub documentation](https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch). This can be constructed using the _[RequestQueryBuilder](#RequestQueryBuilder)_.

* `rows` (_int_)

    Number of rows to return from the API [Reference to documentation](https://scihub.copernicus.eu/userguide/OpenSearchAPI#Paging_results)

* `order_by` (_Optional[str]_)

    Field to order the results on [Reference to documentation](https://scihub.copernicus.eu/userguide/OpenSearchAPI#Sorting_results)

* `start` (_int_)

    Start position of the records to return [Reference to documentation](https://scihub.copernicus.eu/userguide/OpenSearchAPI#Paging_results)

* `username` (_str_)

    Valid username to use to authenticate with the Sentinel Hub API

* `password` (_str_)

    Valid password to use to authenticate with the Sentinel Hub API
</p>
</details>

---

<details id="QuerySentinelProductsResponse">
<summary><strong>QuerySentinelProductsResponse</strong></summary>

<p>

### QuerySentinelProductsResponse (`NamedTuple`/`class`)

Represents the result from the Sentinel Hub API

Can be interacted with as an object or in a more functional style using
the 'on' methods (`on_success`/`on_failure`).

<details>
<summary><strong>Property Details</strong></summary>

<p>

* `status_code` (_Optional[int]_)

    The HTTP Status code representing the outcome of the query

* `body` (_Optional[Dict[str, Any]]_)

    The resulting data from the Sentinel Hub

* `error` (_Optional[BaseException]_)

    An error object if there was an error or exception raised

* `success` (_bool_)

    Whether or not the query was successful
</p>
</details>


<details>
<summary><strong>Method details</strong></summary>

<p>

##### `raise_error`

If encountered an error raise error encountered. Otherwise do nothing

Situations this would be useful:

- Prevent exceptions being swallowed
- You prefer to handle exception rather than checking if value is None

**Returns**: _None_

**Raises**: Error that was encountered when querying the API

---

##### `on_success`

A functional style method for handling successful results. When the action was successful, calls
the supplied function with data from Sentinel Hub API and returns the `QuerySentinelProductsResponse`
so that other methods can be chained

**Parameters**:

* `callback`: (_`Callable[[Dict[str, Any]], None]`_)

    Function which defines the successful behaviour

**Returns**: `QuerySentinelProductsResponse` _self_

---

##### `on_failure`

A functional style method for handling cases where the API was not reachable or
there was an error either in the response or parsing the response, i.e. the request
was not successful.

**Parameters**:

* `callback`: (_`Callable[[QuerySentinelProductsResponse], None]`_)

    Function which defines the failure behaviour, which will be called with named tuple representing the
    result

**Returns**: `QuerySentinelProductsResponse` _self_

<details>
<summary><strong>Example</strong></summary>

<p>

```python
from sentinelpy import QuerySentinelProductsResponse

# You can use the attributes of the response in a more object fashion
# Successful response:
successful_response = QuerySentinelProductsResponse(200, {})

assert successful_response.success
assert successful_response.status_code == 200
assert successful_response.body == {}
assert successful_response.error is None

# Failed response:
failed_response = QuerySentinelProductsResponse(400, {})
assert not failed_response.success
assert failed_response.status_code == 400
assert failed_response.body == {}
assert failed_response.error is None

# Erroneous response
erroneous_response = QuerySentinelProductsResponse(None, None, IOError())
assert not erroneous_response.success
assert erroneous_response.status_code is None
assert erroneous_response.body is None
assert isinstance(erroneous_response.error, IOError)

# Using the functional style methods
successful_response.on_success(
    lambda data: print(f'success:{data}')
).on_failure(
    lambda failure_response: print(f'failure:{failure_response.status_code}')
) # success:{}

failed_response.on_success(
    lambda data: print(f'success:{data}')
).on_failure(
    lambda failure_response: print(f'failure:{failure_response.status_code}')
) # failure:400
```
</p>
</details>

</p>
</details>
</p>
</details>

---

<details id="Enumerations">
<summary><strong>Enumerations</strong></summary>

<p>

In order to simplify validation there are some Enumerations representing some of the types in the `RequestQueryBuilder`, each
valid option maps to a value defined by the API. [Refer to the Sentinel Hub API documentation for more information about the values](https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch)

The enumerations are as follows:

* `OrbitDirection`
* `PlatformName`
* `PolarisationMode`
* `ProductType`
* `SensorOperationalMode`
* `Sentinel1ProductType`
* `Sentinel2ProductType`
* `Sentinel3ProductType`
* `Sentinel5PProductType`
* `SwathIdentifier`
* `Timeliness`

</p>
</details>

# Features

* Queries the Sentinel Hub for products
* Define your requests using the `RequestQueryBuilder` and `SentinelProductRequestBuilder` objects

# Development Documentation

Built using Poetry.

`poetry install`

To install the library locally from source

# Credits

This package was created with Cookiecutter and the `UKHO/cookiecutter-pypackage` project template.

* Cookiecutter: https://github.com/cookiecutter/cookiecutter
* UKHO/cookiecutter-pypackage: https://github.com/UKHO/cookiecutter-pypackage
