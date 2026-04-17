"""Shopping cart module."""

import requests


class Cart:
    """Shopping cart class."""

    def __init__(self):
        """Initialize empty cart."""
        self.items = []

    def add_item(self, name: str, price: float) -> None:
        """Add item to cart."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self) -> float:
        """Calculate total price."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent: float) -> None:
        """Apply discount to all items."""
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be 0-100")
        for item in self.items:
            item["price"] *= 1 - percent / 100


def log_purchase(item: dict) -> None:
    """Log purchase to remote system."""
    requests.post("https://example.com/log", json=item, timeout=5)


COUPONS = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart: Cart, code: str) -> None:
    """Apply coupon to cart."""
    if code not in COUPONS:
        raise ValueError("Invalid coupon")
    cart.apply_discount(COUPONS[code])
