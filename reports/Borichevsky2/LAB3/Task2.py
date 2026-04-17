from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Optional, List
from uuid import uuid4


# ==================== ПОДСИСТЕМЫ ====================

class PassportSystem:
    """
    Подсистема: Паспортные данные.
    Управляет персональной информацией гражданина.
    """

    @dataclass
    class PassportData:
        full_name: str
        birth_date: datetime
        passport_number: str
        issue_date: datetime
        expiry_date: datetime
        nationality: str = "Российская Федерация"
        registration_address: Optional[str] = None

    def __init__(self):
        self._database: dict[str, 'PassportSystem.PassportData'] = {}

    def register_passport(self, full_name: str, birth_date: datetime,
                          passport_number: str,
                          registration_address: Optional[str] = None) -> str:
        """Регистрация нового паспорта."""
        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=365 * 10)  # 10 лет

        data = self.PassportData(
            full_name=full_name,
            birth_date=birth_date,
            passport_number=passport_number,
            issue_date=issue_date,
            expiry_date=expiry_date,
            registration_address=registration_address
        )

        citizen_id = str(uuid4())
        self._database[citizen_id] = data
        return citizen_id

    def verify_identity(self, citizen_id: str) -> bool:
        """Проверка подлинности личности."""
        return citizen_id in self._database

    def get_passport_info(self, citizen_id: str) -> Optional[dict]:
        """Получение паспортных данных."""
        if citizen_id not in self._database:
            return None

        data = self._database[citizen_id]
        return {
            "full_name": data.full_name,
            "passport_number": data.passport_number,
            "expiry_date": data.expiry_date.strftime("%d.%m.%Y"),
            "nationality": data.nationality
        }

    def update_registration(self, citizen_id: str,
                            new_address: str) -> bool:
        """Обновление адреса регистрации."""
        if citizen_id not in self._database:
            return False

        self._database[citizen_id].registration_address = new_address
        return True


class InsuranceSystem:
    """
    Подсистема: Страховой полис (ОМС/ДМС).
    Управляет медицинским страхованием.
    """

    class InsuranceType(Enum):
        OMS = auto()  # Обязательное медицинское страхование
        DMS = auto()  # Добровольное медицинское страхование

    @dataclass
    class InsurancePolicy:
        policy_number: str
        insurance_type: 'InsuranceSystem.InsuranceType'
        company_name: str
        issue_date: datetime
        expiry_date: datetime
        coverage_amount: float

    def __init__(self):
        self._policies: dict[str, 'InsuranceSystem.InsurancePolicy'] = {}

    def create_policy(self, insurance_type: InsuranceType,
                      company_name: str,
                      coverage_amount: float = 0.0) -> str:
        """Создание страхового полиса."""
        policy_number = f"OMS-{uuid4().hex[:8].upper()}"

        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=365)  # 1 год

        policy = self.InsurancePolicy(
            policy_number=policy_number,
            insurance_type=insurance_type,
            company_name=company_name,
            issue_date=issue_date,
            expiry_date=expiry_date,
            coverage_amount=coverage_amount
        )

        self._policies[policy_number] = policy
        return policy_number

    def verify_policy(self, policy_number: str) -> bool:
        """Проверка действительности полиса."""
        if policy_number not in self._policies:
            return False

        policy = self._policies[policy_number]
        return datetime.now() < policy.expiry_date

    def get_policy_info(self, policy_number: str) -> Optional[dict]:
        """Получение информации о полисе."""
        if policy_number not in self._policies:
            return None

        policy = self._policies[policy_number]
        return {
            "number": policy.policy_number,
            "type": "ОМС" if policy.insurance_type == self.InsuranceType.OMS else "ДМС",
            "company": policy.company_name,
            "valid_until": policy.expiry_date.strftime("%d.%m.%Y"),
            "coverage": policy.coverage_amount
        }


class BankingSystem:
    """
    Подсистема: Банковская карта.
    Управляет финансовыми операциями.
    """

    class CardType(Enum):
        DEBIT = auto()
        CREDIT = auto()
        PREPAID = auto()

    @dataclass
    class BankCard:
        card_number: str
        card_type: 'BankingSystem.CardType'
        balance: float = 0.0
        credit_limit: float = 0.0
        is_blocked: bool = False
        transactions: List[dict] = field(default_factory=list)

    def __init__(self):
        self._cards: dict[str, 'BankingSystem.BankCard'] = {}

    def issue_card(self, card_type: CardType,
                   initial_balance: float = 0.0,
                   credit_limit: float = 0.0) -> str:
        """Выпуск банковской карты."""
        # Генерация номера карты (16 цифр)
        card_number = "".join([str(uuid4().int % 10) for _ in range(16)])
        card_number = " ".join([card_number[i:i + 4] for i in range(0, 16, 4)])

        card = self.BankCard(
            card_number=card_number,
            card_type=card_type,
            balance=initial_balance,
            credit_limit=credit_limit
        )

        self._cards[card_number] = card
        return card_number

    def get_balance(self, card_number: str) -> Optional[float]:
        """Получение баланса."""
        if card_number not in self._cards:
            return None
        return self._cards[card_number].balance

    def deposit(self, card_number: str, amount: float) -> bool:
        """Пополнение счета."""
        if card_number not in self._cards or amount <= 0:
            return False

        self._cards[card_number].balance += amount
        self._log_transaction(card_number, "DEPOSIT", amount)
        return True

    def withdraw(self, card_number: str, amount: float) -> bool:
        """Снятие средств."""
        if card_number not in self._cards:
            return False

        card = self._cards[card_number]
        available = card.balance + card.credit_limit

        if amount <= 0 or available < amount:
            return False

        card.balance -= amount
        self._log_transaction(card_number, "WITHDRAW", amount)
        return True

    def _log_transaction(self, card_number: str,
                         operation: str, amount: float) -> None:
        """Логирование транзакции."""
        self._cards[card_number].transactions.append({
            "date": datetime.now().isoformat(),
            "operation": operation,
            "amount": amount,
            "balance": self._cards[card_number].balance
        })


class TransportSystem:
    """
    Подсистема: Транспортная карта.
    Управляет проездными и балансом для транспорта.
    """

    FARE_SINGLE = 57.0  # Стоимость одной поездки

    def __init__(self):
        self._transport_cards: dict[str, dict] = {}

    def issue_transport_card(self) -> str:
        """Выпуск транспортной карты."""
        card_id = f"TR-{uuid4().hex[:10].upper()}"
        self._transport_cards[card_id] = {
            "balance": 0.0,
            "trips_remaining": 0,
            "last_trip": None
        }
        return card_id

    def top_up(self, card_id: str, amount: float) -> bool:
        """Пополнение баланса."""
        if card_id not in self._transport_cards:
            return False

        self._transport_cards[card_id]["balance"] += amount
        return True

    def pay_fare(self, card_id: str) -> tuple[bool, str]:
        """Оплата проезда."""
        if card_id not in self._transport_cards:
            return False, "Карта не найдена"

        card = self._transport_cards[card_id]

        # Приоритет: поездки по абонементу
        if card["trips_remaining"] > 0:
            card["trips_remaining"] -= 1
            card["last_trip"] = datetime.now().isoformat()
            return True, "Оплачено по абонементу"

        # Оплата с баланса
        if card["balance"] >= self.FARE_SINGLE:
            card["balance"] -= self.FARE_SINGLE
            card["last_trip"] = datetime.now().isoformat()
            return True, f"Оплачено {self.FARE_SINGLE} руб."

        return False, "Недостаточно средств"

    def buy_subscription(self, card_id: str, trips: int) -> bool:
        """Покупка абонемента на поездки."""
        if card_id not in self._transport_cards:
            return False

        cost = trips * 50  # Скидка при покупке пакета
        card = self._transport_cards[card_id]

        if card["balance"] < cost:
            return False

        card["balance"] -= cost
        card["trips_remaining"] += trips
        return True


# ==================== ФАСАД ====================

class UniversalElectronicCard:
    """
    Фасад: Универсальная электронная карта.

    Предоставляет единый упрощенный интерфейс к сложной системе
    подсистем: паспорт, страховка, банк, транспорт.
    """

    def __init__(self):
        # Инициализация всех подсистем
        self._passport_system = PassportSystem()
        self._insurance_system = InsuranceSystem()
        self._banking_system = BankingSystem()
        self._transport_system = TransportSystem()

        # Идентификаторы компонентов карты
        self._card_id: Optional[str] = None
        self._citizen_id: Optional[str] = None
        self._policy_number: Optional[str] = None
        self._bank_card_number: Optional[str] = None
        self._transport_card_id: Optional[str] = None

        self._is_activated = False

    # ========== Методы инициализации ==========

    def activate(self, full_name: str, birth_date: datetime,
                 passport_number: str,
                 registration_address: Optional[str] = None) -> str:
        """
        Активация универсальной карты.
        Создает все необходимые компоненты в одном вызове.

        Args:
            full_name: Полное ФИО
            birth_date: Дата рождения
            passport_number: Номер паспорта
            registration_address: Адрес регистрации

        Returns:
            ID универсальной карты
        """
        # Создание паспортных данных
        self._citizen_id = self._passport_system.register_passport(
            full_name, birth_date, passport_number, registration_address
        )

        # Создание страхового полиса (ОМС по умолчанию)
        self._policy_number = self._insurance_system.create_policy(
            InsuranceSystem.InsuranceType.OMS,
            "Росгосстрах Медицина",
            coverage_amount=0.0
        )

        # Выпуск банковской карты (дебетовая)
        self._bank_card_number = self._banking_system.issue_card(
            BankingSystem.CardType.DEBIT,
            initial_balance=0.0
        )

        # Выпуск транспортной карты
        self._transport_card_id = self._transport_system.issue_transport_card()

        # Генерация ID универсальной карты
        self._card_id = f"UEC-{uuid4().hex[:12].upper()}"
        self._is_activated = True

        return self._card_id

    # ========== Упрощенные методы доступа ==========

    def get_personal_info(self) -> Optional[dict]:
        """Получение персональных данных (паспорт)."""
        if not self._is_activated:
            return None
        return self._passport_system.get_passport_info(self._citizen_id)

    def get_insurance_info(self) -> Optional[dict]:
        """Получение информации о страховке."""
        if not self._is_activated:
            return None
        return self._insurance_system.get_policy_info(self._policy_number)

    def get_bank_balance(self) -> Optional[float]:
        """Получение баланса банковской карты."""
        if not self._is_activated:
            return None
        return self._banking_system.get_balance(self._bank_card_number)

    def top_up_bank_account(self, amount: float) -> bool:
        """Пополнение банковского счета."""
        if not self._is_activated:
            return False
        return self._banking_system.deposit(self._bank_card_number, amount)

    def withdraw_cash(self, amount: float) -> bool:
        """Снятие наличных."""
        if not self._is_activated:
            return False
        return self._banking_system.withdraw(self._bank_card_number, amount)

    def pay_for_transport(self) -> tuple[bool, str]:
        """Оплата проезда в транспорте."""
        if not self._is_activated:
            return False, "Карта не активирована"
        return self._transport_system.pay_fare(self._transport_card_id)

    def top_up_transport(self, amount: float) -> bool:
        """Пополнение транспортной карты."""
        if not self._is_activated:
            return False
        return self._transport_system.top_up(self._transport_card_id, amount)

    def verify_card(self) -> dict:
        """
        Комплексная проверка всех компонентов карты.
        Скрывает сложность проверки каждой подсистемы.
        """
        if not self._is_activated:
            return {"status": "error", "message": "Карта не активирована"}

        return {
            "status": "ok",
            "card_id": self._card_id,
            "passport_valid": self._passport_system.verify_identity(
                self._citizen_id
            ),
            "insurance_valid": self._insurance_system.verify_policy(
                self._policy_number
            ),
            "bank_balance": self.get_bank_balance(),
            "components": {
                "passport": self.get_personal_info(),
                "insurance": self.get_insurance_info(),
                "bank_card": self._mask_card_number(self._bank_card_number),
                "transport": self._transport_card_id
            }
        }

    def _mask_card_number(self, card_number: str) -> str:
        """Маскирование номера карты для безопасности."""
        parts = card_number.split()
        return f"**** **** **** {parts[-1]}"

    def get_full_report(self) -> str:
        """Полный отчет о состоянии карты."""
        verification = self.verify_card()

        if verification["status"] == "error":
            return verification["message"]

        report = [
            "=" * 50,
            "УНИВЕРСАЛЬНАЯ ЭЛЕКТРОННАЯ КАРТА",
            f"ID: {self._card_id}",
            "=" * 50,
            "",
            "📋 ПАСПОРТНЫЕ ДАННЫЕ:",
            f"  ФИО: {verification['components']['passport']['full_name']}",
            f"  Гражданство: {verification['components']['passport']['nationality']}",
            "",
            "🏥 СТРАХОВОЙ ПОЛИС:",
            f"  Номер: {verification['components']['insurance']['number']}",
            f"  Тип: {verification['components']['insurance']['type']}",
            f"  Действует до: {verification['components']['insurance']['valid_until']}",
            "",
            "💳 БАНКОВСКАЯ КАРТА:",
            f"  Номер: {verification['components']['bank_card']}",
            f"  Баланс: {verification['bank_balance']} руб.",
            "",
            "🚌 ТРАНСПОРТНАЯ КАРТА:",
            f"  ID: {verification['components']['transport']}",
            "",
            "✅ Статус: Активна" if self._is_activated else "❌ Статус: Не активна",
            "=" * 50
        ]

        return "\n".join(report)


# ============== Демонстрация работы ==============

def main():
    """Демонстрация работы паттерна FACADE."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА FACADE")
    print("Универсальная Электронная Карта")
    print("=" * 60)

    # Создание и активация карты
    print("\n1. Активация новой универсальной карты...")
    print("-" * 50)

    uec = UniversalElectronicCard()
    card_id = uec.activate(
        full_name="Иванов Иван Иванович",
        birth_date=datetime(1990, 5, 15),
        passport_number="4515 123456",
        registration_address="г. Москва, ул. Примерная, д. 1"
    )
    print(f"Карта активирована! ID: {card_id}")

    # Проверка статуса
    print("\n2. Проверка компонентов карты...")
    print("-" * 50)
    status = uec.verify_card()
    print(f"Паспорт действителен: {status['passport_valid']}")
    print(f"Страховка действительна: {status['insurance_valid']}")

    # Финансовые операции
    print("\n3. Финансовые операции...")
    print("-" * 50)
    print(f"Текущий баланс: {uec.get_bank_balance()} руб.")

    print("Пополнение на 5000 руб...")
    uec.top_up_bank_account(5000)
    print(f"Баланс после пополнения: {uec.get_bank_balance()} руб.")

    print("Снятие 1200 руб...")
    uec.withdraw_cash(1200)
    print(f"Баланс после снятия: {uec.get_bank_balance()} руб.")

    # Транспорт
    print("\n4. Транспортные операции...")
    print("-" * 50)
    print("Пополнение транспортной карты на 1000 руб...")
    uec.top_up_transport(1000)

    print("Оплата проезда:")
    for i in range(3):
        success, message = uec.pay_for_transport()
        status = "✓" if success else "✗"
        print(f"  {status} Поездка {i + 1}: {message}")

    # Полный отчет
    print("\n5. Полный отчет о карте...")
    print("-" * 50)
    print(uec.get_full_report())

    print("\n" + "=" * 60)
    print("Готово!")
    print("=" * 60)


if __name__ == "__main__":
    main()