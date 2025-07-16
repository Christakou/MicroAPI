from dataclasses import dataclass, field
from typing import Literal
from venv import logger

HTTP_201 = "201 Created"
HTTP_200 = "200 OK"
HTTP_404 = "404 Not Found"


@dataclass
class HTTPRequest:
    path: str
    verb: Literal["POST", "GET", "PUT", "DELETE"]
    body: str
    headers: dict[str, str]

    @classmethod
    def from_bytes(cls, raw_request:bytes) -> 'HTTPRequest':
        try:
            request_lines = raw_request.decode('utf-8').split("\r\n")
            verb, path, _ = request_lines[0].split()
            header_lines = request_lines[1:-2]
            headers = {line.split(":")[0].strip():line.split(":")[1].strip() for line in header_lines}
            body = request_lines[-1]

            parsed_request = HTTPRequest(path, verb, body, headers)
            logger.info(f" Successfully parsed request: \n {parsed_request}")

            return parsed_request

        except Exception as e:
            raise Exception("Error encountered while parsing request") from e


@dataclass
class HTTPResponse:
    status_code: Literal["200 Ok", "201 Created", "404 Not Found"]
    headers: dict[str, str] = field(default_factory=lambda: {
        "Content-Type": "text/plain",
        "Content-Length": "0"
    })
    body: str = ""

    def to_bytes(self) -> bytes:
        rendered_response = f"""HTTP/1.1 {self.status_code}\r\n"""
        for header, value in self.headers.items():
            rendered_response += f"{header}: {value}\r\n"
        rendered_response += "\r\n" + self.body
        return rendered_response.encode('utf-8')
