import os
from venv import logger
from microapi.models import HTTP_201, HTTP_404, HTTPRequest, HTTPResponse, HTTP_200

def empty_handler(request: HTTPRequest) -> HTTPResponse:
    """
    A simple handler that returns a 200 OK response with an empty body.
    """
    return HTTPResponse(
        status_code=HTTP_200,
        body="",
        headers={
            "Content-Length": "0",
            "Content-Type": "text/plain"
        }
    )

def echo_handler(request: HTTPRequest) -> HTTPResponse:
    """
    A simple echo handler that returns the request body.
    """
    to_return = request.path.replace("/echo/", "")
    return HTTPResponse(
        status_code=HTTP_200,
        body=to_return,
        headers={
            "Content-Length":str(len(to_return)),
            "Content-Type":"text/plain"
        }

    )


def user_agent_handler(request: HTTPRequest) -> HTTPResponse:
    response = HTTPResponse(
        status_code=HTTP_200,
        headers={"Content-Type":"text/plain",
                 "Content-Length":len(request.headers.get("User-Agent",""))},
        body=request.headers.get("User-Agent","")
    )
    return response

def post_file_handler(request: HTTPRequest) -> HTTPResponse:
    """
    Handles POST requests to upload a file to the server.
    """
    file_path = request.path.replace("/files/", os.environ.get("FILE_DIR"))
    try:
        with open(file_path, 'wb') as f:
            f.write(request.body.encode('utf-8'))
            return HTTPResponse(
                status_code=HTTP_201,
                body="File uploaded successfully",
                headers={"Content-Type": "text/plain"}
            )
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return HTTPResponse(
            status_code=HTTP_404,
            body="Failed to upload file",
            headers={"Content-Type": "text/plain"}
        )

def get_file_handler(request: HTTPRequest)-> HTTPResponse:
    """
    Returns a file from the server.
    """
    file_path = request.path.replace("/files/", os.environ.get("FILE_DIR"))
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            return HTTPResponse(
                status_code=HTTP_200,
                body=content.decode('utf-8'),
                headers={
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(len(content))
                }
            )
    except FileNotFoundError:
        return HTTPResponse(
            status_code=HTTP_404,
            body="File not found",
            headers={"Content-Type": "text/plain"}
        )