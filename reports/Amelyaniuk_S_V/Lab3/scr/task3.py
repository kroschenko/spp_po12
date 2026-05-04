from abc import ABC, abstractmethod


# --- Интерфейс Состояния ---
class ATMState(ABC):
    @abstractmethod
    def enter_pin(self, atm, pin: str):
        pass

    @abstractmethod
    def withdraw(self, atm, amount: int):
        pass

    @abstractmethod
    def finish(self, atm):
        pass


# --- Конкретные состояния ---


class IdleState(ATMState):
    """Состояние ожидания"""

    def enter_pin(self, atm, pin: str):
        print(f"[ATM {atm.id}] Пин-код введен. Переход к аутентификации...")
        atm.set_state(AuthState())
        atm.enter_pin(pin)  # Вызываем проверку в новом состоянии

    def withdraw(self, atm, amount: int):
        print("Ошибка: Сначала введите пин-код!")

    def finish(self, atm):
        print("Банкомат уже находится в режиме ожидания.")


class AuthState(ATMState):
    """Состояние аутентификации"""

    def enter_pin(self, atm, pin: str):
        if pin == "1234":
            print("Пин-код верный. Доступ разрешен.")
            atm.set_state(TransactionState())
        else:
            print("Неверный пин-код! Возврат в режим ожидания.")
            atm.set_state(IdleState())

    def withdraw(self, atm, amount: int):
        print("Ошибка: Сначала подтвердите пин-код!")

    def finish(self, atm):
        atm.set_state(IdleState())


class TransactionState(ATMState):
    """Состояние выполнения операций"""

    def enter_pin(self, atm, pin: str):
        print("Вы уже авторизованы.")

    def withdraw(self, atm, amount: int):
        if amount <= atm.total_money:
            atm.total_money -= amount
            print(f"Выдано: {amount} руб. Остаток в банкомате: {atm.total_money} руб.")
            if atm.total_money <= 0:
                atm.set_state(BlockedState())
        else:
            print("В банкомате недостаточно средств для совершения операции!")

    def finish(self, atm):
        print("Сессия завершена. Заберите карту.")
        atm.set_state(IdleState())


class BlockedState(ATMState):
    """Состояние блокировки (нет денег)"""

    def enter_pin(self, atm, pin: str):
        print("Банкомат заблокирован: нет наличных.")

    def withdraw(self, atm, amount: int):
        print("Извините, в банкомате закончились деньги.")

    def finish(self, atm):
        print("Банкомат не обслуживает клиентов.")


# --- Контекст (Класс Банкомат) ---
class ATM:
    def __init__(self, atm_id: str, initial_money: int):
        self.id = atm_id
        self.total_money = initial_money
        # Начальное состояние зависит от наличия денег
        if self.total_money > 0:
            self._state = IdleState()
        else:
            self._state = BlockedState()

    def set_state(self, state: ATMState):
        self._state = state

    # Методы-делегаты, которые перенаправляют вызов текущему состоянию
    def enter_pin(self, pin: str):
        self._state.enter_pin(self, pin)

    def withdraw(self, amount: int):
        self._state.withdraw(self, amount)

    def finish(self):
        self._state.finish(self)


# --- Тестирование работы ---
if __name__ == "__main__":
    my_atm = ATM(atm_id="SBER-001", initial_money=5000)

    print(f"--- Работа с банкоматом {my_atm.id} ---")

    # Попытка снять без пина
    my_atm.withdraw(1000)

    # Авторизация и снятие
    my_atm.enter_pin("1234")
    my_atm.withdraw(2000)
    my_atm.finish()

    print("\n--- Новая сессия (Снятие всей суммы) ---")
    my_atm.enter_pin("1234")
    my_atm.withdraw(3000)  # Денег больше нет

    print("\n--- Попытка работы после опустошения ---")
    my_atm.enter_pin("1234")
