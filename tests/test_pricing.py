import pytest

from app.pricing import apply_discount, order_total


def test_no_discount():
    assert apply_discount(100.0, 0) == 100.0


def test_ten_percent_discount():
    assert apply_discount(200.0, 10) == 180.0


def test_order_total_with_discount():
    assert order_total([(10.0, 2), (5.0, 4)], discount_percent=25) == 30.0


def test_invalid_percent():
    with pytest.raises(ValueError):
        apply_discount(100.0, 101)
