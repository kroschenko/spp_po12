"""
Модуль для управления корзиной покупок и логирования операций.
Лабораторная работа №6.
"""
import requests

class Cart:
    """
    Класс, представляющий корзину покупок.
    """
    def __init__(self):
        """Инициализация пустого списка товаров."""
        self.items = []

    def add_item(self, name, price):
        """Добавляет товар в корзину. Выбрасывает ValueError, если цена < 0."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Возвращает общую стоимость всех товаров в корзине."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount_percent):
        """Применяет скидку в процентах ко всем товарам в корзине."""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Недопустимое значение скидки")

        factor = 1 - (discount_percent / 100)
        for item in self.items:
            item["price"] *= factor

def log_purchase(item):
    """Отправляет данные о покупке на удаленный сервер."""
    # Добавлен timeout=5, чтобы pylint не ругался на возможное зависание
    requests.post("https://example.com/log", json=item, timeout=5)

# Словарь купонов вынесен на уровень модуля для удобного мокинга
coupons = {"SAVE10": 10, "HALF": 50}

def apply_coupon(cart, coupon_code):
    """Применяет скидку к корзине на основании кода купона."""
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
