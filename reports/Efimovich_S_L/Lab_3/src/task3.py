class ATM:
    def __init__(self, atm_id, initial_money):
        self.id = atm_id
        self.total_money = initial_money
        self.card_inserted = False
        self.authenticated = False
        self.state = WaitingState(self)

    def set_state(self, state):
        self.state = state

    def insert_card(self):
        self.state.insert_card()

    def enter_pin(self, pin):
        self.state.enter_pin(pin)

    def withdraw(self, amount):
        self.state.withdraw(amount)

    def cancel(self):
        self.state.cancel()

    def get_state_name(self):
        return self.state.__class__.__name__


class ATMState:
    def __init__(self, atm):
        self.atm = atm

    def insert_card(self):
        print("Операция недоступна в текущем режиме")

    def enter_pin(self, pin):
        print(f"Операция недоступна в текущем режиме {pin}")

    def withdraw(self, amount):
        print(f"Операция недоступна в текущем режиме {amount}")

    def cancel(self):
        print("Операция недоступна в текущем режиме")


class WaitingState(ATMState):
    def insert_card(self):
        print("Карта вставлена. Введите пин-код")
        self.atm.card_inserted = True
        self.atm.set_state(PinAuthState(self.atm))


class PinAuthState(ATMState):
    def __init__(self, atm):
        super().__init__(atm)
        self.attempts = 0

    def enter_pin(self, pin):
        if pin == "1234":
            print("Пин-код верный")
            self.atm.authenticated = True
            self.atm.set_state(OperationState(self.atm))
        else:
            self.attempts += 1
            print(f"Неверный пин-код. Попытка {self.attempts}/3")
            if self.attempts >= 3:
                print("Слишком много попыток. Карта заблокирована")
                self.atm.set_state(BlockedState(self.atm))

    def cancel(self):
        print("Операция отменена. Заберите карту")
        self.atm.card_inserted = False
        self.atm.set_state(WaitingState(self.atm))


class OperationState(ATMState):
    def withdraw(self, amount):
        if amount <= 0:
            print("Сумма должна быть положительной")
            return

        if amount > self.atm.total_money:
            print(f"Недостаточно средств в банкомате. Доступно: {self.atm.total_money}")
            self.atm.set_state(BlockedState(self.atm))
            return

        if amount > 10000:
            print("Сумма превышает лимит на одну операцию")
            return

        self.atm.total_money -= amount
        print(f"Выдано {amount} руб. Остаток в банкомате: {self.atm.total_money}")

        if self.atm.total_money == 0:
            print("В банкомате закончились деньги")
            self.atm.set_state(BlockedState(self.atm))

    def cancel(self):
        print("Сеанс завершен. Заберите карту")
        self.atm.card_inserted = False
        self.atm.authenticated = False
        self.atm.set_state(WaitingState(self.atm))


class BlockedState(ATMState):
    def insert_card(self):
        print("Банкомат временно не работает. Попробуйте позже")

    def enter_pin(self, pin):
        print("Банкомат временно не работает")

    def withdraw(self, amount):
        print("Банкомат временно не работает")

    def cancel(self):
        print("Возврат в начальный режим")
        self.atm.card_inserted = False
        self.atm.authenticated = False
        self.atm.set_state(WaitingState(self.atm))


if __name__ == "__main__":
    atmClass = ATM("ATM-001", 50000)

    print(f"Банкомат {atmClass.id} запущен. Денег: {atmClass.total_money}")
    print("-" * 40)

    atmClass.insert_card()
    atmClass.enter_pin("1111")
    atmClass.enter_pin("2222")
    atmClass.enter_pin("1234")

    atmClass.withdraw(5000)
    atmClass.withdraw(20000)
    atmClass.withdraw(30000)

    atmClass.cancel()
    print(f"Состояние: {atmClass.get_state_name()}")

    print("\n" + "-" * 40)
    print("Тест блокировки при отсутствии денег:")

    atmClass.insert_card()
    atmClass.enter_pin("1234")
    atmClass.withdraw(25000)
    atmClass.withdraw(1000)
    atmClass.cancel()
