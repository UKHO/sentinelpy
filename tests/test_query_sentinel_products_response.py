from unittest.mock import Mock

from assertpy import assert_that, fail

from query_sentinel_products.exceptions import QuerySentinelProductsError
from query_sentinel_products.query_sentinel_products_response import (
    QuerySentinelProductsResponse,
)


class TestQuerySentinelProductsResponse:
    def test_when_response_then_can_get_data_back(self):
        success_response = QuerySentinelProductsResponse(200, {})

        assert_that(success_response.status_code).is_equal_to(200)
        assert_that(success_response.body).is_equal_to({})
        assert_that(success_response.error).is_equal_to(None)

    def test_when_success_response_then_raise_error_does_nothing(self):
        success_response = QuerySentinelProductsResponse(200, {})

        try:
            success_response.raise_error()
        except Exception as exception:
            fail(f"Unexpected exception: {exception}")

    def test_when_error_response_then_raises_error(self):
        error = QuerySentinelProductsError(ValueError(), 200, "not json")

        error_response = QuerySentinelProductsResponse(200, None, error)

        assert_that(error_response.raise_error).raises(
            QuerySentinelProductsError
        ).when_called_with()

    def test_when_success_response_then_success_is_true(self):
        success_response = QuerySentinelProductsResponse(200, {})

        assert_that(success_response.success).is_true()

    def test_when_error_response_then_success_is_false(self):
        error = QuerySentinelProductsError(ValueError(), 200, "not json")

        error_response = QuerySentinelProductsResponse(200, None, error)

        assert_that(error_response.success).is_false()

    def test_when_non_2xx_status_code_then_success_is_false(self):
        error_response = QuerySentinelProductsResponse(400, None, None)

        assert_that(error_response.success).is_false()

    def test_when_success_and_on_success_called_then_calls_callback(self):
        callback = Mock()

        success_response = QuerySentinelProductsResponse(200, {"data": {}})
        success_response.on_success(callback)

        callback.assert_called_once_with({"data": {}})

    def test_when_error_and_on_success_called_then_does_not_call_callback(self):
        callback = Mock()

        error = QuerySentinelProductsError(ValueError(), 200, "not json")

        error_response = QuerySentinelProductsResponse(200, None, error)
        error_response.on_success(callback)

        callback.assert_not_called()

    def test_when_call_has_non_200_code_on_success_then_does_not_call_callback(self):
        callback = Mock()

        response = QuerySentinelProductsResponse(400, None, None)
        response.on_success(callback)

        callback.assert_not_called()

    def test_when_on_success_call_then_returns_response(self):
        callback = Mock()

        response = QuerySentinelProductsResponse(400, None, None)
        result = response.on_success(callback)

        assert_that(result).is_equal_to(response)

    def test_when_success_and_on_failure_called_then_does_not_call_callback(self):
        callback = Mock()

        success_response = QuerySentinelProductsResponse(200, {"data": {}})
        success_response.on_failure(callback)

        callback.assert_not_called()

    def test_when_error_and_on_failure_called_then_calls_callback(self):
        callback = Mock()

        error = QuerySentinelProductsError(ValueError(), 200, "not json")

        error_response = QuerySentinelProductsResponse(200, None, error)
        error_response.on_failure(callback)

        callback.assert_called_once_with(
            QuerySentinelProductsResponse(200, None, error)
        )

    def test_when_call_has_non_200_code_on_failure_then_calls_callback(self):
        callback = Mock()

        response = QuerySentinelProductsResponse(400, {"data": {}}, None)
        response.on_failure(callback)

        callback.assert_called_once_with(
            QuerySentinelProductsResponse(400, {"data": {}}, None)
        )

    def test_when_on_failure_call_then_returns_response(self):
        callback = Mock()

        response = QuerySentinelProductsResponse(400, None, None)
        result = response.on_failure(callback)

        assert_that(result).is_equal_to(response)

    def test_when_methods_chained_and_success_then_calls_correct_callback(self):
        correct_cb = Mock()
        incorrect_cb = Mock()

        QuerySentinelProductsResponse(200, {"data": {}}).on_success(
            correct_cb
        ).on_failure(incorrect_cb)

        correct_cb.assert_called_once()
        incorrect_cb.assert_not_called()

    def test_when_methods_chained_and_error_then_calls_correct_callback(self):
        correct_cb = Mock()
        incorrect_cb = Mock()

        error = QuerySentinelProductsError(ValueError(), 200, "not json")

        QuerySentinelProductsResponse(200, None, error).on_success(
            incorrect_cb
        ).on_failure(correct_cb)

        correct_cb.assert_called_once()
        incorrect_cb.assert_not_called()

    def test_when_methods_chained_and_failure_then_calls_correct_callback(self):
        correct_cb = Mock()
        incorrect_cb = Mock()

        QuerySentinelProductsResponse(400, None, None).on_success(
            incorrect_cb
        ).on_failure(correct_cb)

        correct_cb.assert_called_once()
        incorrect_cb.assert_not_called()

    def test_when_has_error_and_bad_status_then_treated_as_error(self):
        correct_cb = Mock()
        incorrect_cb = Mock()

        QuerySentinelProductsResponse(400, None, ValueError).on_success(
            incorrect_cb
        ).on_failure(correct_cb)

        correct_cb.assert_called_once()
        incorrect_cb.assert_not_called()

    def test_when_has_error_and_good_status_then_treated_as_error(self):
        correct_cb = Mock()
        incorrect_cb = Mock()

        QuerySentinelProductsResponse(200, None, ValueError).on_success(
            incorrect_cb
        ).on_failure(correct_cb)

        correct_cb.assert_called_once()
        incorrect_cb.assert_not_called()
