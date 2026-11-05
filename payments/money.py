"""Money helpers. Every amount in this service is an integer number of cents."""
from decimal import ROUND_HALF_UP, Decimal


def to_cents(amount: str) -> int:
    """Parse a decimal string such as "12.30" into cents."""
    value = Decimal(amount)
    if value != value.quantize(Decimal("0.01")):
        raise ValueError(f"more than two decimal places: {amount!r}")
    return int(value * 100)


def apply_rate(cents: int, rate_bp: int) -> int:
    """Apply a rate given in basis points (725 = 7.25%), rounded half up to the cent."""
    exact = Decimal(cents) * Decimal(rate_bp) / Decimal(10000)
    return int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def format_cents(cents: int, currency: str = "USD") -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d} {currency}"
