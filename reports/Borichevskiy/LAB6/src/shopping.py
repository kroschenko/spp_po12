"""
Мини‑библиотека покупок для тестирования.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass
class Item:
    name: str
    price: float


class Cart:
    """Корзина покупок."""

    def __init__(self) -> None:
        self.items: Dict[str, float] = {}

    def add_item(self, name: str, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items[name] = price

    def total(self) -> float:
        return sum(self.items.values())

    def apply_discount(self, percent: float) -> None:
        if percent < 0 or percent > 100:
            raise ValueError("Invalid discount")
        factor = 1 - percent / 100
        for name in list(self.items):
            self.items[name] = round(self.items[name] * factor, 2)


def log_purchase(item: dict) -> None:
    """
    Логирование покупки в удалённую систему.
    В тестах requests.post будет замокан.
    """
    import requests

    requests.post("https://example.com/log", json=item)


def apply_coupon(cart: Cart, coupon_code: str) -> None:
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code not in coupons:
        raise ValueError("Invalid coupon")
    cart.apply_discount(coupons[coupon_code])
