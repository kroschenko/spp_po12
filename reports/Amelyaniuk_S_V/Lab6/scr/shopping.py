import requests


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent):
        if not (0 <= percent <= 100):
            raise ValueError("Неверный процент скидки")
        for item in self.items:
            item["price"] *= 1 - percent / 100


def log_purchase(item):
    requests.post("https://example.com/log", json=item)


def apply_coupon(cart, coupon_code):
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
