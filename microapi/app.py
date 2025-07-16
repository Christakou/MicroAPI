import socket  # noqa: F401
from collections.abc import Callable
import threading
import re
from typing import Dict
from concurrent.futures import ThreadPoolExecutor
from microapi.middleware import MiddleWare, RouteHandler, BaseMiddleWare
from microapi.models import HTTP_404, HTTPRequest, HTTPResponse


class App:
    def __init__(self, host="localhost", port=4221):
        self.host = host
        self.port = port
        self.routes: Dict[str, RouteHandler] = {}
        self.middleware_stack: list[MiddleWare] = [BaseMiddleWare()]
        self.thread_pool: ThreadPoolExecutor =  ThreadPoolExecutor(max_workers=3)

    def register_middleware(self, middleware: MiddleWare):
        """
        Register a middleware with the app.
        """
        self.middleware_stack.append(middleware)

    def start(self):
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        print(f"Server started at http://{self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                self.thread_pool.submit(self.handle_client, client_socket)

        except KeyboardInterrupt:
            print("Server stopped.")
        finally:
            server_socket.close()
        return server_socket

    def add_route(self, method: str, path_pattern: str, handler: RouteHandler):
        """
        Register a route with the app.
        """
        self.routes[(method, path_pattern)] = handler


    def handle_client(self, client_socket: socket.socket):
        request = client_socket.recv(1024)
        if not request:
            client_socket.close()
            return
        response = self.handle_request(request)
        client_socket.sendall(response)
        client_socket.close()

    def handle_request(self, request_raw: bytes) -> bytes:

        request = HTTPRequest.from_bytes(request_raw)
        for (route_verb, path_pattern), handler in self.routes.items():
            if request.verb == route_verb and re.fullmatch(path_pattern, request.path):
                return handler.__call__(request).to_bytes()
        # If no route matches, return 404 Not Found
        return HTTPResponse(status_code=HTTP_404).to_bytes()



