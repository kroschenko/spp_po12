#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Payment System for Infocommunication Organization
Demonstrates OOP principles: inheritance, abstraction, encapsulation, polymorphism
"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum


class PaymentStatus(Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class AccountStatus(Enum):
    """Account status enumeration"""
    ACTIVE = "active"
    BLOCKED = "blocked"
    CLOSED = "closed"


class CardStatus(Enum):
    """Card status enumeration"""
    ACTIVE = "active"
    BLOCKED = "blocked"


# ==================== SYSTEM CLASSES ====================


class Order:
    """Order class (association with Client)"""

    def __init__(self, order_id: str, amount: float, description: str):
        self.order_id = order_id
        self.amount = amount
        self.description = description
        self.is_paid = False

    def __str__(self) -> str:
        status = "paid" if self.is_paid else "unpaid"
        return f"Order {self.order_id}: {self.description}, {self.amount} RUB ({status})"


class CreditCard:
    """Credit card class (aggregation with Client)"""

    def __init__(self, card_number: str, limit: float):
        self.card_number = card_number
        self.limit = limit
        self.balance = 0.0
        self.status = CardStatus.ACTIVE

    @property
    def available_credit(self) -> float:
        return self.limit - self.balance

    def charge(self, amount: float) -> bool:
        if self.status == CardStatus.BLOCKED:
            print(f"Card {self.card_number}: operation declined (card blocked)")
            return False
        if amount > self.available_credit:
            print(f"Card {self.card_number}: insufficient funds")
            return False
        self.balance += amount
        print(f"Card {self.card_number}: charged {amount} RUB")
        return True

    def block(self) -> None:
        self.status = CardStatus.BLOCKED
        print(f"Card {self.card_number}: blocked")

    def __str__(self) -> str:
        return (
            f"Card {self.card_number}: limit={self.limit}, "
            f"debt={self.balance}, status={self.status.value}"
        )


class BankAccount:
    """Bank account class"""

    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self._balance = initial_balance
        self.status = AccountStatus.ACTIVE

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> bool:
        if self.status != AccountStatus.ACTIVE:
            print(f"Account {self.account_number}: operation not allowed")
            return False
        self._balance += amount
        print(f"Account {self.account_number}: deposited {amount} RUB")
        return True

    def withdraw(self, amount: float) -> bool:
        if self.status != AccountStatus.ACTIVE:
            print(f"Account {self.account_number}: operation not allowed")
            return False
        if amount > self._balance:
            print(f"Account {self.account_number}: insufficient funds")
            return False
        self._balance -= amount
        print(f"Account {self.account_number}: withdrew {amount} RUB")
        return True

    def close(self) -> None:
        self.status = AccountStatus.CLOSED
        print(f"Account {self.account_number}: closed")

    def __str__(self) -> str:
        return (
            f"Account {self.account_number}: balance={self._balance}, "
            f"status={self.status.value}"
        )


class User(ABC):
    """Abstract user class"""

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self) -> str:
        pass


class Client(User):
    """Client class"""

    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name)
        self.account: Optional[BankAccount] = None
        self.credit_card: Optional[CreditCard] = None

    def get_role(self) -> str:
        return "Client"

    def assign_account(self, new_account: BankAccount) -> None:
        self.account = new_account
        print(f"{self.name}: assigned {new_account}")

    def assign_card(self, new_card: CreditCard) -> None:
        self.credit_card = new_card
        print(f"{self.name}: assigned {new_card}")

    def pay_order(self, order_obj: Order) -> bool:
        if not self.account:
            print(f"{self.name}: no account assigned")
            return False

        print(f"\n--- Paying order {order_obj.order_id} ---")
        if self.account.withdraw(order_obj.amount):
            order_obj.is_paid = True
            print(f"Order {order_obj.order_id} paid!")
            return True
        return False

    def pay_order_by_card(self, order_obj: Order) -> bool:
        if not self.credit_card:
            print(f"{self.name}: no card assigned")
            return False

        print(f"\nPaying order {order_obj.order_id} with card")
        if self.credit_card.charge(order_obj.amount):
            order_obj.is_paid = True
            print(f"Order {order_obj.order_id} paid by card!")
            return True
        return False

    def transfer_to_account(self, target_account: BankAccount, sum_to_transfer: float) -> bool:
        if not self.account:
            print(f"{self.name}: no account assigned")
            return False

        print(
            f"\nTransferring {sum_to_transfer} RUB "
            f"to account {target_account.account_number}"
        )
        if self.account.withdraw(sum_to_transfer):
            target_account.deposit(sum_to_transfer)
            print("Transfer completed!")
            return True
        return False

    def block_own_card(self) -> None:
        if self.credit_card:
            self.credit_card.block()

    def close_account(self) -> None:
        if self.account:
            self.account.close()
            self.account = None


class Administrator(User):
    """Administrator class"""

    def get_role(self) -> str:
        return "Administrator"

    def block_card_for_debt(self, target_card: CreditCard) -> None:
        if target_card.balance >= target_card.limit:
            print(
                f"\n[ADMIN] Blocking card {target_card.card_number} "
                f"due to limit exceeded"
            )
            target_card.block()
        else:
            print(
                f"\n[ADMIN] Card {target_card.card_number} is OK, "
                f"no blocking required"
            )


# ==================== DEMONSTRATION ====================

if __name__ == "__main__":
    print("=" * 60)
    print("TASK 2: PAYMENT SYSTEM DEMONSTRATION")
    print("=" * 60)

    client1 = Client("C001", "Ivan Petrov")
    admin = Administrator("A001", "System Admin")

    print(f"\n{client1}")
    print(f"{admin}")

    account1 = BankAccount("40817810000000000001", 10000.0)
    account2 = BankAccount("40817810000000000002", 5000.0)
    card1 = CreditCard("4276123456789012", 50000.0)

    print("\nAssigning accounts and cards")
    client1.assign_account(account1)
    client1.assign_card(card1)

    order1 = Order("ORD-001", 3000.0, "Laptop")
    order2 = Order("ORD-002", 500.0, "Mouse")

    print(f"\n{order1}")
    print(f"{order2}")

    client1.pay_order(order1)
    print(f"\nCurrent account balance: {account1.balance} RUB")

    client1.pay_order_by_card(order2)
    print(f"\nCurrent card debt: {card1.balance} RUB")

    client1.transfer_to_account(account2, 2000.0)
    print(f"\nAccount 1 balance: {account1.balance} RUB")
    print(f"Account 2 balance: {account2.balance} RUB")

    print("\n--- Simulating credit limit exceed ---")
    big_order = Order("ORD-003", 50000.0, "Car")
    client1.pay_order_by_card(big_order)

    admin.block_card_for_debt(card1)

    order3 = Order("ORD-004", 1000.0, "Fuel")
    client1.pay_order_by_card(order3)

    print("\n--- Closing account ---")
    client1.close_account()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
