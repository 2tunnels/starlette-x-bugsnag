try:
    from importlib import metadata
except ImportError:  # pragma: no cover
    import importlib_metadata as metadata  # type:ignore

from typing import Any

from bugsnag.client import Client
from bugsnag.notification import Notification
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class BugsnagMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, api_key: str, **kwargs: Any):
        dispatch = kwargs.pop("dispatch", None)

        super().__init__(app, dispatch)

        self._client = Client(api_key=api_key, **kwargs)
        self._configure_packages_tab()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            self._client.notify(
                exc,
                context=request.url,
                severity="error",
                scope=request.scope,
                locals=self._get_locals(exc),
            )

            raise exc

    @staticmethod
    def _get_packages() -> dict:
        return {
            dist.metadata["Name"]: dist.metadata["Version"]
            for dist in metadata.distributions()
        }

    @staticmethod
    def _get_locals(exception: Exception) -> dict:
        """Return local variables from exception last traceback frame."""

        tb = exception.__traceback__

        if not tb:
            return {}

        while tb.tb_next is not None:
            tb = tb.tb_next

        return tb.tb_frame.f_locals

    def _configure_packages_tab(self) -> None:
        packages = self._get_packages()

        def add_packages_tab(notification: Notification) -> None:
            notification.add_tab("packages", packages)

        self._client.configuration.middleware.before_notify(add_packages_tab)
