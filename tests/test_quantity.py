import decimal
import pytest

from lightkube.utils.quantity import parse_quantity


def test_unitless():
    """Unitless values must be interpreted as decimal notation."""
    assert parse_quantity("1.5") == decimal.Decimal("1.5")
    assert parse_quantity("-1.5") == decimal.Decimal("-1.5")
    assert parse_quantity("0.30000000000000004") == decimal.Decimal("0.301")
    assert parse_quantity("0.09999999999999998") == decimal.Decimal("0.1")
    assert parse_quantity("3.141592653") == decimal.Decimal("3.142")


def test_binary_notation():
    assert parse_quantity("1.5Gi") == parse_quantity("1536Mi") == decimal.Decimal("1610612736")
    assert parse_quantity("0.9Gi") == decimal.Decimal("966367641.6")


def test_decimal_notation():
    assert parse_quantity("1.5G") == decimal.Decimal("1500000000")
    assert parse_quantity("0.9G") == decimal.Decimal("900000000")
    assert parse_quantity("500m") == decimal.Decimal("0.5")


def test_none():
    assert parse_quantity(None) is None


def test_invalid_value():
    with pytest.raises(ValueError):
        parse_quantity("1.2.3")
    with pytest.raises(ValueError):
        parse_quantity("1e2.3")
    with pytest.raises(ValueError):
        # decimal.InvalidOperation
        parse_quantity("9e999")
    with pytest.raises(ValueError):
        # decimal.Overflow
        parse_quantity("9e9999999")


def test_invalid_unit():
    with pytest.raises(ValueError):
        parse_quantity("1kb")
    with pytest.raises(ValueError):
        parse_quantity("1GGi")


def test_whitespace():
    with pytest.raises(ValueError):
        parse_quantity("")
    with pytest.raises(ValueError):
        parse_quantity(" ")
    with pytest.raises(ValueError):
        parse_quantity("1 ")
    with pytest.raises(ValueError):
        parse_quantity(" 1")
    with pytest.raises(ValueError):
        parse_quantity("1 Gi")
