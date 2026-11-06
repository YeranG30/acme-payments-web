import pytest

from payments.checkout import CheckoutError, quote


def cart(**over):
    base = {
        "items": [{"sku": "mug", "quantity": 2, "unit_cents": 1250}, {"sku": "tee", "quantity": 1, "unit_cents": 1999}],
        "region": "US-CA",
        "discount_code": "WELCOME10",
    }
    base.update(over)
    return base


def test_quote_with_discount_and_tax():
    q = quote(cart())
    assert q == {"subtotal_cents": 4499, "discount_cents": 450, "tax_cents": 294, "total_cents": 4343}


def test_tax_rounds_once_on_the_cart_total():
    # Three lines of 0.05 each in Texas: per-line rounding would charge 0 tax, the cart total is 0.15 -> 0.01
    q = quote(cart(items=[{"sku": "sticker", "quantity": 1, "unit_cents": 5}] * 3, region="US-TX", discount_code="LOYAL5"))
    assert q["tax_cents"] == 1


@pytest.mark.parametrize("region,tax", [("US-NY", 162), ("GB", 810), ("DE", 769)])
def test_regions(region, tax):
    assert quote(cart(region=region))["tax_cents"] == tax


@pytest.mark.parametrize(
    "bad",
    [
        {"items": []},
        {"region": "FR"},
        {"discount_code": "NOPE"},
        {"items": [{"sku": "mug", "quantity": 0, "unit_cents": 1250}]},
        {"items": [{"sku": "mug", "quantity": 1, "unit_cents": -1}]},
    ],
)
def test_invalid_carts(bad):
    with pytest.raises(CheckoutError):
        quote(cart(**bad))


def test_discount_code_is_normalised():
    assert quote(cart(discount_code=" welcome10 ")) == quote(cart(discount_code="WELCOME10"))


@pytest.mark.parametrize("code", [None, "", "   "])
def test_missing_discount_code_means_no_discount(code):
    assert quote(cart(discount_code=code))["discount_cents"] == 0
