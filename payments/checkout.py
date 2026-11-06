"""Checkout quotes: subtotal, discount and tax for a cart."""
from .money import apply_rate

# Sales tax by region, in basis points.
TAX_RATES_BP = {
    "US-CA": 725,
    "US-NY": 400,
    "US-TX": 625,
    "GB": 2000,
    "DE": 1900,
}

# Active discount codes, in basis points off the subtotal.
DISCOUNT_CODES = {
    "WELCOME10": 1000,
    "LOYAL5": 500,
}

MAX_QUANTITY = 99


class CheckoutError(ValueError):
    """The cart is invalid. Shown to the customer as a 400."""


def _line_total(item: dict) -> int:
    qty = item.get("quantity")
    unit = item.get("unit_cents")
    if not isinstance(qty, int) or not 1 <= qty <= MAX_QUANTITY:
        raise CheckoutError(f"quantity must be 1-{MAX_QUANTITY}")
    if not isinstance(unit, int) or unit < 0:
        raise CheckoutError("unit_cents must be a non-negative integer")
    return qty * unit


def quote(cart: dict) -> dict:
    items = cart.get("items") or []
    if not items:
        raise CheckoutError("cart is empty")
    region = cart.get("region")
    if region not in TAX_RATES_BP:
        raise CheckoutError(f"unsupported region: {region!r}")

    subtotal = sum(_line_total(item) for item in items)

    # Codes arrive from the web form with stray spaces and in any case.
    code = (cart.get("discount_code") or "").strip().upper()
    discount = 0
    if code:
        if code not in DISCOUNT_CODES:
            raise CheckoutError(f"unknown discount code: {code!r}")
        discount = apply_rate(subtotal, DISCOUNT_CODES[code])

    taxable = subtotal - discount
    tax = apply_rate(taxable, TAX_RATES_BP[region])
    return {
        "subtotal_cents": subtotal,
        "discount_cents": discount,
        "tax_cents": tax,
        "total_cents": taxable + tax,
    }
