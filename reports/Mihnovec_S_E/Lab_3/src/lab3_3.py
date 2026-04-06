"""
Модуль реализует паттерн проектирования 'Состояние' (State).
Моделирует работу банкомата с различными режимами:
ожидание, аутентификация, выполнение операций и блокировка.
"""

from abc import ABC, abstractmethod


class ATMState(ABC):
    """
    Абстрактный базовый класс для состояний банкомата.
    Определяет интерфейс для всех конкретных состояний.
    """

    @abstractmethod
    def enter_pin(self, atm_context, pin: str):
        """Метод для обработки ввода пин-кода."""

    @abstractmethod
    def withdraw(self, atm_context, amount: float):
        """Метод для обработки снятия наличных."""

    @abstractmethod
    def finish(self, atm_context):
        """Метод для завершения сессии."""


class WaitingState(ATMState):
    """
    Состояние ожидания ввода пин-кода.
    """

    def enter_pin(self, atm_context, pin: str):
        """Проверяет пин-код и переводит банкомат в режим операций."""
        if pin == "1234":
            print("Пин-код верный. Переход в меню операций.")
            atm_context.set_state(OperationState())
        else:
            print("Неверный пин-код.")

    def withdraw(self, atm_context, amount: float):
        """В этом состоянии снятие невозможно."""
        print("Сначала введите пин-код.")

    def finish(self, atm_context):
        """Завершение не требуется, так как сессия не начата."""
        print("Вы и так на стартовом экране.")


class OperationState(ATMState):
    """
    Состояние выполнения операций (пользователь авторизован).
    """

    def enter_pin(self, atm_context, pin: str):
        """Повторный ввод пин-кода не требуется."""
        print("Вы уже авторизованы.")

    def withdraw(self, atm_context, amount: float):
        """Проверяет баланс банкомата и выдает деньги."""
        if amount > atm_context.total_money:
            print("Ошибка: В банкомате недостаточно средств!")
        else:
            atm_context.total_money -= amount
            print(f"Выдано {amount} руб. Остаток: {atm_context.total_money} руб.")
            if atm_context.total_money <= 0:
                print("В банкомате закончились деньги. Блокировка.")
                atm_context.set_state(LockedState())

    def finish(self, atm_context):
        """Завершает сессию и возвращает в режим ожидания."""
        print("Завершение работы. Заберите карту.")
        atm_context.set_state(WaitingState())


class LockedState(ATMState):
    """
    Состояние блокировки (деньги в банкомате закончились).
    """

    def enter_pin(self, atm_context, pin: str):
        """Запрет любых действий."""
        print("Банкомат заблокирован (нет денег).")

    def withdraw(self, atm_context, amount: float):
        """Запрет любых действий."""
        print("Банкомат заблокирован (нет денег).")

    def finish(self, atm_context):
        """Запрет любых действий."""
        print("Банкомат заблокирован (нет денег).")


class ATM:
    """
    Класс контекста (Банкомат), который делегирует выполнение
    методов текущему состоянию.
    """

    def __init__(self, atm_id: str, total_money: float):
        self.atm_id = atm_id
        self.total_money = total_money
        self.state = WaitingState()

    def set_state(self, state: ATMState):
        """Меняет текущее состояние банкомата."""
        self.state = state

    def enter_pin(self, pin: str):
        """Вызывает ввод пина у текущего состояния."""
        self.state.enter_pin(self, pin)

    def withdraw(self, amount: float):
        """Вызывает снятие у текущего состояния."""
        self.state.withdraw(self, amount)

    def finish(self):
        """Вызывает завершение у текущего состояния."""
        self.state.finish(self)

    def get_info(self):
        """Возвращает информацию о банкомате."""
        return f"ATM ID: {self.atm_id}, Баланс: {self.total_money}"


def main():
    """
    Основная функция для демонстрации работы паттерна Состояние.
    """
    print("--- Задача 3: Состояние ---")
    my_atm = ATM(atm_id="ATM-001", total_money=1000.0)

    print(my_atm.get_info())
    my_atm.withdraw(100)
    my_atm.enter_pin("1234")
    my_atm.withdraw(800)
    my_atm.withdraw(200)
    my_atm.finish()


if __name__ == "__main__":
    main()
