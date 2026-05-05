"""Модуль с классами и функциями для работы с корзиной покупок."""
import requests


class Cart:
    """Класс для представления корзины покупок."""

    def __init__(self):
        """Инициализирует пустую корзину."""
        self.items = []

    def add_item(self, name, price):
        """Добавляет товар в корзину с заданной ценой.

        Args:
            name: Название товара.
            price: Цена товара (неотрицательная).

        Raises:
            ValueError: Если цена отрицательная.
        """
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Возвращает общую стоимость всех товаров в корзине."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent):
        """Применяет скидку ко всем товарам в корзине.

        Args:
            percent: Процент скидки (0-100).

        Raises:
            ValueError: Если процент скидки вне диапазона 0-100.
        """
        if not 0 <= percent <= 100:
            raise ValueError("Неверный процент скидки")
        for item in self.items:
            item["price"] *= 1 - percent / 100


def log_purchase(item):
    """Логирует информацию о покупке на удаленный сервер.

    Args:
        item: Словарь с информацией о товаре.
    """
    requests.post("https://example.com/log", json=item, timeout=30)


def apply_coupon(cart, coupon_code):
    """Применяет купон к корзине покупок.

    Args:
        cart: Объект корзины Cart.
        coupon_code: Код купона для применения.

    Raises:
        ValueError: Если купон невалиден.
    """
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
