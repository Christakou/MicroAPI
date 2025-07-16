from abc import abstractmethod
from typing import Protocol, Callable

from microapi.models import HTTPRequest, HTTPResponse


class MiddleWare(Protocol):
    def __call__(self, request: HTTPRequest, call_next: Callable[[HTTPRequest], HTTPResponse]) -> Callable[[HTTPRequest], HTTPResponse]:
        """
        """
        pass


class RouteHandler(Protocol):
    @abstractmethod
    def __call__(self, request: HTTPRequest) -> HTTPResponse:
        """
        Handle an HTTP request and return an HTTP response.
        """
        pass


class BaseMiddleWare(MiddleWare):
    def __call__(self, request: HTTPRequest, call_next: Callable[[HTTPRequest], HTTPResponse]) -> HTTPResponse:
        """
        Base middleware that can be extended to add custom functionality.
        """
        # Call the next handler in the middleware chain
        response = call_next(request)
        print("Middleware processing request:", request.path)
        return response
