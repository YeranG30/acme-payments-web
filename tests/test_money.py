import pytest

from payments.money import apply_rate, format_cents, to_cents


@pytest.mark.parametrize("amount,cents", [("0", 0), ("12.3", 1230), ("12.30", 1230), ("0.05", 5)])
def test_to_cents(amount, cents):
    assert to_cents(amount) == cents


def test_to_cents_rejects_fractions_of_a_cent():
    with pytest.raises(ValueError):
        to_cents("1.005")


@pytest.mark.parametrize("cents,rate,expected", [(1000, 725, 73), (200, 625, 13), (1, 5000, 1), (0, 1900, 0)])
def test_apply_rate_rounds_half_up(cents, rate, expected):
    assert apply_rate(cents, rate) == expected


def test_format_cents():
    assert format_cents(123456) == "1234.56 USD"
    assert format_cents(-5, "EUR") == "-0.05 EUR"
