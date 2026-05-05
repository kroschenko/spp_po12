"""Модуль мини-библиотеки покупок."""

from dataclasses import dataclass

import requests

COUPONS = {"SAVE10": 10, "HALF": 50}


@dataclass(frozen=True)
class CartItem:
    """Элемент корзины с названием и ценой."""

    name: str
    price: float


class Cart:
    """Корзина покупок."""

    def __init__(self) -> None:
        """Создаёт пустую корзину."""
        self.items: list[CartItem] = []

    def add_item(self, name: str, price: float) -> None:
        """Добавляет товар в корзину."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append(CartItem(name=name, price=float(price)))

    def total(self) -> float:
        """Возвращает общую стоимость корзины."""
        return sum(item.price for item in self.items)

    def apply_discount(self, percent: float) -> None:
        """Применяет скидку к каждому товару в корзине."""
        if percent < 0 or percent > 100:
            raise ValueError("Скидка должна быть в диапазоне от 0 до 100")
        factor = 1 - percent / 100
        self.items = [
            CartItem(name=item.name, price=item.price * factor) for item in self.items
        ]


def log_purchase(item: dict[str, object]) -> None:
    """Отправляет информацию о покупке в удалённую систему."""
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart: Cart, coupon_code: str) -> None:
    """Применяет купон к корзине."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
        return
    raise ValueError("Invalid coupon")
