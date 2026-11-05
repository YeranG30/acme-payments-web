"""Health check: drive the app in-process with the carts in scripts/smoke_carts.json.

    python -m scripts.smoke [--json]

Exit 0 when every request answers below 500, 1 otherwise. The deploy and health-check workflows run this and
post the result to the status issue.
"""
import io
import json
import sys
from pathlib import Path
from wsgiref.util import setup_testing_defaults

from payments.app import application

CARTS = json.loads((Path(__file__).parent / "smoke_carts.json").read_text())


def request(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else b""
    env = {"REQUEST_METHOD": method, "PATH_INFO": path, "CONTENT_LENGTH": str(len(data)), "wsgi.input": io.BytesIO(data)}
    setup_testing_defaults(env)
    status = {}
    b"".join(application(env, lambda s, h: status.setdefault("code", int(s.split()[0]))))
    return status["code"]


def main():
    results = [("health", request("GET", "/health"))]
    results += [(f"checkout: {c['name']}", request("POST", "/checkout", c["cart"])) for c in CARTS]
    failed = [r for r in results if r[1] >= 500]
    if "--json" in sys.argv:
        print(json.dumps({"ok": not failed, "results": [{"check": n, "status": s} for n, s in results]}))
    else:
        for name, status in results:
            print(f"{'FAIL' if status >= 500 else 'ok  '} {status} {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
