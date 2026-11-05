# acme-payments-web

Backend for the payments web app: checkout quotes (subtotal, discount codes, sales tax).

```
GET  /health     liveness and version
POST /checkout   {"items": [{"sku", "quantity", "unit_cents"}], "region": "US-CA", "discount_code": "WELCOME10"}
```

## Develop

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
python -m scripts.smoke      # the health check production runs
```

## Ship

`main` deploys to **staging** automatically. **Production** is a manual run of `Deploy production`, which waits
for an approval in the `production` environment. See [CONTRIBUTING.md](CONTRIBUTING.md). Status page: the pinned
**Production status** issue.
