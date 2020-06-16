from unittest.mock import MagicMock

from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.testclient import TestClient


def test_without_exception(
    bugsnag_delivery: MagicMock,
    bugsnag_client_constructor: MagicMock,
    test_client: TestClient,
) -> None:
    response = test_client.get("/good")

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"message": "Hello world!"}

    bugsnag_client_constructor.assert_called_once_with(api_key="secret")
    bugsnag_delivery.deliver.assert_not_called()


def test_with_exception(
    bugsnag_delivery: MagicMock,
    bugsnag_client_constructor: MagicMock,
    test_client: TestClient,
) -> None:
    response = test_client.get("/bad")

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == "Internal Server Error"

    bugsnag_client_constructor.assert_called_once_with(api_key="secret")
    bugsnag_delivery.deliver.assert_called_once()
