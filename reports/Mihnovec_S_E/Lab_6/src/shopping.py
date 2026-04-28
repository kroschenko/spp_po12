"""Модуль для управления корзиной покупок."""
from typing import Dict
import requests

COUPONS: Dict[str, float] = {"SAVE10": 10, "HALF": 50}


class Cart:
    """Класс корзины покупок."""

    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        """Добавляет товар в корзину."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self) -> float:
        """Возвращает общую стоимость товаров."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount: float):
        """Применяет скидку в процентах."""
        if not 0 <= discount <= 100:
            raise ValueError("Скидка должна быть от 0 до 100")
        for item in self.items:
            item["price"] *= (100 - discount) / 100


def log_purchase(item: dict):
    """Логирует покупку через POST запрос."""
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart: Cart, coupon_code: str):
    """Применяет купон к корзине."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
