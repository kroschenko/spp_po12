"""Модуль корзины покупок и работы с купонами."""

import requests


class Cart:
    """Класс для управления товарами в корзине."""

    def __init__(self):
        """Инициализация пустой корзины."""
        self.items = []

    def add_item(self, name, price):
        """Добавляет товар в корзину."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Возвращает общую стоимость товаров."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent):
        """Применяет скидку ко всем товарам в корзине."""
        if not 0 <= percent <= 100:
            raise ValueError("Скидка должна быть от 0 до 100")

        discount_factor = (100 - percent) / 100
        for item in self.items:
            item["price"] *= discount_factor


def log_purchase(item):
    """Отправляет лог о покупке на сервер."""
    requests.post("https://example.com/log", json=item, timeout=5)


COUPONS = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    """Применяет купон к корзине."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
