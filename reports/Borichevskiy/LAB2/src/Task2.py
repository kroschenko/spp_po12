#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Payment System — демонстрация ООП в стиле лабораторной работы.
"""

from abc import ABC, abstractmethod
from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"


class CardStatus(Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class Order:
    """Заказ клиента."""

    def __init__(self, order_id: str, amount: float, description: str):
        self.order_id = order_id
        self.amount = amount
        self.description = description
        self.is_paid = False

    def __str__(self) -> str:
        status = "paid" if self.is_paid else "unpaid"
        return f"{self.order_id}: {self.description} ({self.amount} RUB, {status})"


class CreditCard:
    """Кредитная карта."""

    def __init__(self, number: str, limit_value: float):
        self.number = number
        self.limit = limit_value
        self.balance = 0
        self.status = CardStatus.ACTIVE

    @property
    def available(self) -> float:
        return self.limit - self.balance

    def charge(self, amount: float) -> bool:
        if self.status == CardStatus.BLOCKED:
            return False
        if amount > self.available:
            return False
        self.balance += amount
        return True

    def block(self) -> None:
        self.status = CardStatus.BLOCKED

    def __str__(self) -> str:
        return f"Card {self.number}: debt={self.balance}, status={self.status.value}"


class BankAccount:
    """Банковский счёт."""

    def __init__(self, number: str, balance: float):
        self.number = number
        self._balance = balance
        self.status = AccountStatus.ACTIVE

    @property
    def balance(self) -> float:
        return self._balance

    def withdraw(self, amount: float) -> bool:
        if self.status != AccountStatus.ACTIVE:
            return False
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def deposit(self, amount: float) -> bool:
        if self.status != AccountStatus.ACTIVE:
            return False
        self._balance += amount
        return True

    def close(self) -> None:
        self.status = AccountStatus.CLOSED

    def __str__(self) -> str:
        return f"Account {self.number}: balance={self._balance}, status={self.status.value}"


class User(ABC):
    """Абстрактный пользователь."""

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self) -> str:
        pass


class Client(User):
    """Клиент."""

    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name)
        self.account = None
        self.card = None

    def get_role(self) -> str:
        return "Client"

    def assign_account(self, account: BankAccount) -> None:
        self.account = account

    def assign_card(self, card: CreditCard) -> None:
        self.card = card

    def pay(self, order: Order) -> bool:
        if not self.account:
            return False
        if self.account.withdraw(order.amount):
            order.is_paid = True
            return True
        return False

    def pay_by_card(self, order: Order) -> bool:
        if not self.card:
            return False
        if self.card.charge(order.amount):
            order.is_paid = True
            return True
        return False


class Administrator(User):
    """Администратор."""

    def get_role(self) -> str:
        return "Administrator"

    def block_if_needed(self, card: CreditCard) -> None:
        if card.balance >= card.limit:
            card.block()


if __name__ == "__main__":
    client = Client("C01", "Ivan")
    acc = BankAccount("ACC-1", 5000)
    card = CreditCard("CARD-1", 10000)

    client.assign_account(acc)
    client.assign_card(card)

    order = Order("ORD-1", 1500, "Phone")

    print("Оплата заказа:", client.pay(order))
    print(order)

