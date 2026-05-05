"""
Мини-библиотека покупок.
Обеспечивает работу с корзиной, товарами, скидками и купонами.
"""

import requests

coupons = {"SAVE10": 10, "HALF": 50}


class Cart:
    """Класс, представляющий корзину покупок клиента."""

    def __init__(self):
        """Инициализация пустой корзины."""
        self.items = []

    def add_item(self, name: str, price: float) -> None:
        """Добавляет новый товар в корзину. Выбрасывает ошибку при отрицательной цене."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self) -> float:
        """Вычисляет общую стоимость всех товаров в корзине."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount: float) -> None:
        """Применяет процентную скидку ко всем товарам в корзине."""
        if discount < 0 or discount > 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")

        factor = (100 - discount) / 100
        for item in self.items:
            item["price"] *= factor


def log_purchase(item: dict) -> None:
    """Отправляет лог с информацией о покупке на удаленный сервер."""
    requests.post("https://example.com/log", json=item, timeout=10)


def apply_coupon(cart: Cart, coupon_code: str) -> None:
    """Применяет скидку к корзине на основе переданного промокода."""
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
