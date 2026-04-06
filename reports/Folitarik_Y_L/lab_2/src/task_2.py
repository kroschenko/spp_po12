"""
Модуль для имитации банковской системы.
Содержит классы для управления клиентами, счетами, картами и банком.
"""

import uuid
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Card:
    """
    Класс, представляющий банковскую карту.
    Используется декоратор dataclass, чтобы избежать R0903.
    """

    card_id: str
    bank_account_id: int
    name: str
    balance: float = 0.0
    is_blocked: bool = False


class BankAccount:
    """Класс, представляющий банковский счет клиента."""

    def __init__(self, account_id: int):
        """Инициализация счета."""
        self.cards: List[Card] = []
        self.account_id = account_id

    def add_card(self, name: str, initial_balance: float = 0.0) -> Card:
        """Создает и добавляет новую карту к счету."""
        new_card_id = str(uuid.uuid4())
        new_card = Card(new_card_id, self.account_id, name, initial_balance)
        self.cards.append(new_card)
        return new_card

    def get_card_by_name(self, card_name: str) -> Optional[Card]:
        """Поиск карты по имени."""
        for card in self.cards:
            if card.name == card_name:
                return card
        return None

    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """Поиск карты по уникальному идентификатору."""
        for card in self.cards:
            if card.card_id == card_id:
                return card
        return None


class Client:
    """Класс, представляющий клиента банка."""

    def __init__(self, is_admin: bool):
        """Инициализация клиента."""
        self.is_admin = is_admin
        self.bank_account: Optional[BankAccount] = None

    def pay_for_order(self, card_name: str, cost: float) -> bool:
        """Оплата заказа с указанной карты."""
        if not self.bank_account:
            return False

        card = self.bank_account.get_card_by_name(card_name)
        if not card or card.is_blocked or card.balance < cost:
            return False

        card.balance -= cost
        return True

    def make_payment(
        self, source_card_name: str, target_account_id: int, amount: float, bank: "Bank"
    ) -> bool:
        """Перевод средств на другой счет."""
        if not self.bank_account:
            return False

        source_card = self.bank_account.get_card_by_name(source_card_name)
        if not source_card or source_card.is_blocked or source_card.balance < amount:
            return False

        target_account = bank.find_bank_account_by_id(target_account_id)
        if not target_account or not target_account.cards:
            return False

        target_card = target_account.cards[0]
        source_card.balance -= amount
        target_card.balance += amount
        return True

    def block_card(self, card_name: str) -> bool:
        """Блокировка карты самим клиентом."""
        if not self.bank_account:
            return False

        card = self.bank_account.get_card_by_name(card_name)
        if not card:
            return False

        card.is_blocked = True
        return True

    def unblock_card(self, card_name: str) -> bool:
        """Разблокировка карты самим клиентом."""
        if not self.bank_account:
            return False

        card = self.bank_account.get_card_by_name(card_name)
        if not card:
            return False

        card.is_blocked = False
        return True

    def close_account(self, bank: "Bank") -> bool:
        """Закрытие банковского счета клиента."""
        if not self.bank_account:
            return False

        if bank.remove_bank_account(self.bank_account.account_id):
            self.bank_account = None
            return True
        return False


class Bank:
    """Класс, представляющий банк и управляющий счетами."""

    _account_id_counter = 0

    def __init__(self):
        """Инициализация банка."""
        self.bank_accounts: List[BankAccount] = []

    def add_bank_account(self, client: Client) -> Optional[BankAccount]:
        """Создание нового счета для клиента."""
        if isinstance(client, Client):
            Bank._account_id_counter += 1
            new_account = BankAccount(Bank._account_id_counter)
            self.bank_accounts.append(new_account)
            client.bank_account = new_account
            return new_account
        return None

    def find_bank_account_by_id(self, account_id: int) -> Optional[BankAccount]:
        """Поиск счета по его ID."""
        for account in self.bank_accounts:
            if account.account_id == account_id:
                return account
        return None

    def find_card_by_id(self, card_id: str) -> Optional[Card]:
        """Поиск карты по всем счетам банка."""
        for account in self.bank_accounts:
            card = account.get_card_by_id(card_id)
            if card:
                return card
        return None

    def remove_bank_account(self, account_id: int) -> bool:
        """Удаление счета из базы банка."""
        account_to_remove = self.find_bank_account_by_id(account_id)
        if account_to_remove:
            self.bank_accounts.remove(account_to_remove)
            return True
        return False

    def block_card_by_admin(self, admin_client: Client, card_id: str) -> bool:
        """Блокировка любой карты администратором."""
        if not admin_client.is_admin:
            return False

        card = self.find_card_by_id(card_id)
        if not card:
            return False

        card.is_blocked = True
        return True


def main():
    """Точка входа в программу. Демонстрация работы."""
    my_bank = Bank()

    client1 = Client(is_admin=False)
    client2 = Client(is_admin=False)
    admin = Client(is_admin=True)

    acc1 = my_bank.add_bank_account(client1)
    acc2 = my_bank.add_bank_account(client2)
    my_bank.add_bank_account(admin)

    if acc1:
        acc1.add_card("MainCard_C1", 1000.0)
        acc1.add_card("Savings_C1", 500.0)
    if acc2:
        acc2.add_card("Primary_C2", 200.0)

    cost = 150.0
    if client1.pay_for_order("MainCard_C1", cost):
        print("Оплата прошла успешно")
    else:
        print("Ошибка оплаты")

    if client1.block_card("Savings_C1"):
        print("Карта Savings_C1 заблокирована")


if __name__ == "__main__":
    main()
