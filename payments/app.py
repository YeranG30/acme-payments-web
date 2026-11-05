"""The HTTP service (plain WSGI, so it runs behind any server).

    GET  /health     liveness and the running version
    POST /checkout   a quote for a cart (see checkout.quote)
"""
import json
import logging

from . import __version__
from .checkout import CheckoutError, quote

log = logging.getLogger(__name__)


def _json(start_response, status, body):
    data = json.dumps(body).encode()
    start_response(status, [("Content-Type", "application/json"), ("Content-Length", str(len(data)))])
    return [data]


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    try:
        if method == "GET" and path == "/health":
            return _json(start_response, "200 OK", {"status": "ok", "version": __version__})
        if method == "POST" and path == "/checkout":
            length = int(environ.get("CONTENT_LENGTH") or 0)
            cart = json.loads(environ["wsgi.input"].read(length) or b"{}")
            return _json(start_response, "200 OK", quote(cart))
        return _json(start_response, "404 Not Found", {"error": "not found"})
    except (CheckoutError, json.JSONDecodeError) as e:
        return _json(start_response, "400 Bad Request", {"error": str(e)})
    except Exception:
        log.exception("unhandled error on %s %s", method, path)
        return _json(start_response, "500 Internal Server Error", {"error": "internal error"})
