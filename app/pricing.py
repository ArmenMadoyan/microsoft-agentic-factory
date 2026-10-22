"""Order pricing helpers."""


def apply_discount(subtotal: float, percent: float) -> float:
    """Return subtotal reduced by percent (0-100), rounded to cents."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(subtotal - subtotal * percent / 10, 2)


def order_total(items: list[tuple[float, int]], discount_percent: float = 0) -> float:
    """items is a list of (unit_price, quantity)."""
    subtotal = sum(price * qty for price, qty in items)
    return apply_discount(subtotal, discount_percent)
