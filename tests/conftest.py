from unittest.mock import MagicMock

import pytest
from bugsnag.client import Client
from pytest_mock.plugin import MockFixture
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_x_bugsnag.middleware import BugsnagMiddleware


@pytest.fixture
def bugsnag_delivery() -> MagicMock:
    return MagicMock()


@pytest.fixture
def bugsnag_client_constructor(
    bugsnag_delivery: MagicMock, mocker: MockFixture
) -> Client:
    client = Client(api_key="secret", delivery=bugsnag_delivery)

    constructor = mocker.patch("starlette_x_bugsnag.middleware.Client")
    constructor.return_value = client

    return constructor


@pytest.fixture
def application() -> Starlette:
    async def good_handler(request: Request) -> JSONResponse:
        return JSONResponse({"message": "Hello world!"})

    async def bad_handler(request: Request) -> None:
        raise RuntimeError("Something went wrong")

    routes = [
        Route("/good", good_handler),
        Route("/bad", bad_handler),
    ]
    middleware = [Middleware(BugsnagMiddleware, api_key="secret")]

    app = Starlette(routes=routes, middleware=middleware)

    return app


@pytest.fixture
def test_client(application: Starlette) -> TestClient:
    return TestClient(application, raise_server_exceptions=False)
