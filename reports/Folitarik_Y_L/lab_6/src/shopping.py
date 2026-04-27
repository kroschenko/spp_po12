"""
Модуль для управления корзиной покупок и обработки скидок.
"""

import requests

# Вынесено в глобальную переменную для корректного мокинга через monkeypatch
COUPONS = {"SAVE10": 10, "HALF": 50}


class Cart:
    """Класс корзины покупок."""

    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        """Добавляет товар в корзину."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self) -> float:
        """Возвращает общую стоимость товаров."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent: float):
        """Применяет скидку ко всем товарам в корзине."""
        if not 0 <= percent <= 100:
            raise ValueError("Invalid discount percentage")
        for item in self.items:
            item["price"] *= 1 - percent / 100


def log_purchase(item: dict):
    """Логирует покупку во внешнюю систему."""
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart: Cart, coupon_code: str):
    """Применяет скидку по коду купона."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
