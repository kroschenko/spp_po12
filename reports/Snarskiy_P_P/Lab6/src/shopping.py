"""Shopping module"""

import requests


class Cart:
    """Cart class"""

    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        """Add an item to the cart"""
        if price < 0:
            raise ValueError(f"Price cannot be negative: {price}")
        self.items.append({"name": name, "price": price})

    def total(self) -> float:
        """Return the total price of the cart"""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent: float):
        """Apply a discount for each item"""
        if percent < 0 or percent > 100:
            raise ValueError(f"Discount must be between 0 and 100, got {percent}")
        factor = 1 - percent / 100
        for item in self.items:
            item["price"] = round(item["price"] * factor, 10)


def log_purchase(item):
    """Log a purchase"""
    requests.post("https://example.com/log", json=item, timeout=5)


COUPONS = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    """Apply a coupon"""
    coupons = COUPONS
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
