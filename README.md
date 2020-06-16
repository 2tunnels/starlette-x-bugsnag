# starlette-x-bugsnag

Shiny [Bugsnag](https://www.bugsnag.com/) integration for [Starlette](https://www.starlette.io/) framework ✨

![test](https://github.com/2tunnels/starlette-x-bugsnag/workflows/test/badge.svg?branch=master)
![codecov](https://img.shields.io/codecov/c/github/2tunnels/starlette-x-bugsnag/master)
![dependencies](https://img.shields.io/librariesio/release/pypi/starlette-x-bugsnag)
![version](https://img.shields.io/pypi/v/starlette-x-bugsnag.svg)
![pyversions](https://img.shields.io/pypi/pyversions/starlette-x-bugsnag.svg)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)
![license](https://img.shields.io/pypi/l/starlette-x-bugsnag)

[Scope](https://asgi.readthedocs.io/en/latest/specs/main.html#connection-scope) details,
local variables and installed packages will be attached to each event for ease of debugging.

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

`BugsnagMiddleware` accepts same arguments as `bugsnag.configure` function, so you can pass additional information
about your app, such as `app_version`.

```python
application = Starlette(
    routes=routes,
    middleware=[
        Middleware(
            BugsnagMiddleware,
            api_key="secret",
            app_version="1.2.3",
            release_stage="production",
            project_root=None,  # Save traceback not only from the current directory
        ),
    ],
)
```
