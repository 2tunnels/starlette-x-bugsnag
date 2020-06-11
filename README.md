# starlette-x-bugsnag

Shiny Bugsnag integration for Starlette framework ✨

![test](https://github.com/2tunnels/starlette-x-bugsnag/workflows/test/badge.svg?branch=master)
![version](https://img.shields.io/pypi/v/starlette-x-bugsnag.svg)
![pyversions](https://img.shields.io/pypi/pyversions/starlette-x-bugsnag.svg)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)
![license](https://img.shields.io/pypi/l/starlette-x-bugsnag)

Installation:

```sh
pip install starlette-x-bugsnag
```

Usage:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_x_bugsnag.middleware import BugsnagMiddleware


async def home(request: Request) -> JSONResponse:
    return JSONResponse({"message": "Hello world!"})


routes = [Route("/", home)]

# Using application constructor
application = Starlette(
    routes=routes, middleware=[Middleware(BugsnagMiddleware, api_key="secret")],
)

# Or using add_middleware method
application.add_middleware(BugsnagMiddleware, api_key="secret")
```
