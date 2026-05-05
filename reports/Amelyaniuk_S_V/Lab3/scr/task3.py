"""Модуль с реализацией паттерна Состояние для симуляции банкомата."""
from abc import ABC, abstractmethod


class ATMState(ABC):
    """Абстрактный класс состояния банкомата."""

    @abstractmethod
    def enter_pin(self, atm, pin: str):
        """Обрабатывает ввод PIN-кода."""

    @abstractmethod
    def withdraw(self, atm, amount: int):
        """Обрабатывает запрос на снятие денег."""

    @abstractmethod
    def finish(self, atm):
        """Обрабатывает завершение операции."""


class IdleState(ATMState):
    """Состояние ожидания ввода PIN-кода."""

    def enter_pin(self, atm, pin: str):
        """Обрабатывает ввод PIN-кода и переходит к аутентификации."""
        print(f"[ATM {atm.id}] Пин-код введен. Переход к аутентификации...")
        atm.set_state(AuthState())
        atm.enter_pin(pin)

    def withdraw(self, atm, amount: int):
        """Сообщает об ошибке - сначала нужно ввести PIN."""
        print("Ошибка: Сначала введите пин-код!")

    def finish(self, atm):
        """Сообщает, что банкомат уже в режиме ожидания."""
        print("Банкомат уже находится в режиме ожидания.")


class AuthState(ATMState):
    """Состояние аутентификации пользователя."""

    def enter_pin(self, atm, pin: str):
        """Проверяет PIN-код и переходит к транзакции или ожиданию."""
        if pin == "1234":
            print("Пин-код верный. Доступ разрешен.")
            atm.set_state(TransactionState())
        else:
            print("Неверный пин-код! Возврат в режим ожидания.")
            atm.set_state(IdleState())

    def withdraw(self, atm, amount: int):
        """Сообщает об ошибке - сначала нужно подтвердить PIN."""
        print("Ошибка: Сначала подтвердите пин-код!")

    def finish(self, atm):
        """Возвращает банкомат в режим ожидания."""
        atm.set_state(IdleState())


class TransactionState(ATMState):
    """Состояние выполнения операций (снятие денег)."""

    def enter_pin(self, atm, pin: str):
        """Сообщает, что пользователь уже авторизован."""
        print("Вы уже авторизованы.")

    def withdraw(self, atm, amount: int):
        """Обрабатывает снятие денег."""
        if amount <= atm.total_money:
            atm.total_money -= amount
            print(
                f"Выдано: {amount} руб. "
                f"Остаток в банкомате: {atm.total_money} руб."
            )
            if atm.total_money <= 0:
                atm.set_state(BlockedState())
        else:
            print("В банкомате недостаточно средств для совершения операции!")

    def finish(self, atm):
        """Завершает сессию и возвращает в режим ожидания."""
        print("Сессия завершена. Заберите карту.")
        atm.set_state(IdleState())


class BlockedState(ATMState):
    """Состояние блокировки (нет денег в банкомате)."""

    def enter_pin(self, atm, pin: str):
        """Сообщает о блокировке банкомата."""
        print("Банкомат заблокирован: нет наличных.")

    def withdraw(self, atm, amount: int):
        """Сообщает об отсутствии денег."""
        print("Извините, в банкомате закончились деньги.")

    def finish(self, atm):
        """Сообщает о невозможности обслуживания."""
        print("Банкомат не обслуживает клиентов.")


class ATM:
    """Класс банкомата с поддержкой состояний."""

    def __init__(self, atm_id: str, initial_money: int):
        """Инициализирует банкомат с заданным ID и суммой."""
        self.id = atm_id
        self.total_money = initial_money
        if self.total_money > 0:
            self._state = IdleState()
        else:
            self._state = BlockedState()

    def set_state(self, state: ATMState):
        """Устанавливает новое состояние банкомата."""
        self._state = state

    def enter_pin(self, pin: str):
        """Делегирует ввод PIN-кода текущему состоянию."""
        self._state.enter_pin(self, pin)

    def withdraw(self, amount: int):
        """Делегирует снятие денег текущему состоянию."""
        self._state.withdraw(self, amount)

    def finish(self):
        """Делегирует завершение операции текущему состоянию."""
        self._state.finish(self)


if __name__ == "__main__":
    my_atm = ATM(atm_id="SBER-001", initial_money=5000)

    print(f"--- Работа с банкоматом {my_atm.id} ---")

    my_atm.withdraw(1000)

    my_atm.enter_pin("1234")
    my_atm.withdraw(2000)
    my_atm.finish()

    print("\n--- Новая сессия (Снятие всей суммы) ---")
    my_atm.enter_pin("1234")
    my_atm.withdraw(3000)

    print("\n--- Попытка работы после опустошения ---")
    my_atm.enter_pin("1234")
