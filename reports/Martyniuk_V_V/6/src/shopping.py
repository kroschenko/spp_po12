"""
Модуль shopping - мини-библиотека для управления корзиной покупок.

Этот модуль предоставляет класс Cart для управления корзиной товаров,
а также функции для логирования покупок и применения купонов.
"""

import requests


class Cart:
    """
    Класс корзины покупок.

    Позволяет добавлять товары, применять скидки и подсчитывать общую стоимость.
    """

    def __init__(self):
        """Инициализация пустой корзины."""
        self.items = []  # каждый элемент: (name, price)

    def add_item(self, name: str, price: float) -> None:
        """
        Добавление товара в корзину.

        Args:
            name: название товара
            price: цена товара

        Raises:
            ValueError: если цена отрицательная
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append((name, price))

    def total(self) -> float:
        """
        Подсчёт общей стоимости всех товаров в корзине.

        Returns:
            Общая сумма всех товаров
        """
        return sum(price for _, price in self.items)

    def apply_discount(self, percent: float) -> None:
        """
        Применение скидки ко всем товарам в корзине.

        Args:
            percent: процент скидки (0-100)

        Raises:
            ValueError: если процент скидки вне диапазона [0, 100]
        """
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        multiplier = (100 - percent) / 100.0
        self.items = [(name, price * multiplier) for name, price in self.items]

    def __len__(self) -> int:
        """Возвращает количество товаров в корзине."""
        return len(self.items)


def log_purchase(item: dict) -> None:
    """
    Логирование покупки в удалённую систему.

    Args:
        item: словарь с информацией о товаре

    Note:
        Добавлен timeout=30 для предотвращения зависания программы.
    """
    requests.post("https://example.com/log", json=item, timeout=30)


def apply_coupon(cart: Cart, coupon_code: str) -> None:
    """
    Применение купона к корзине.

    Args:
        cart: объект корзины
        coupon_code: код купона

    Raises:
        ValueError: если купон недействителен
    """
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
