import io
import json
from wsgiref.util import setup_testing_defaults

from payments import __version__
from payments.app import application


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else b""
    env = {"REQUEST_METHOD": method, "PATH_INFO": path, "CONTENT_LENGTH": str(len(data)), "wsgi.input": io.BytesIO(data)}
    setup_testing_defaults(env)
    seen = {}

    def start_response(status, headers):
        seen["status"] = int(status.split()[0])

    out = b"".join(application(env, start_response))
    return seen["status"], json.loads(out)


def test_health():
    assert call("GET", "/health") == (200, {"status": "ok", "version": __version__})


def test_checkout():
    status, body = call("POST", "/checkout", {"items": [{"sku": "mug", "quantity": 1, "unit_cents": 1000}],
                                              "region": "US-NY", "discount_code": "LOYAL5"})
    assert status == 200 and body["total_cents"] == 988


def test_checkout_bad_cart_is_400():
    assert call("POST", "/checkout", {"items": []})[0] == 400


def test_unknown_path_is_404():
    assert call("GET", "/nope")[0] == 404
