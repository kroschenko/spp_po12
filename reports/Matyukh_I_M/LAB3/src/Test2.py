from abc import ABC, abstractmethod


class PassportSystem:
    def __init__(self, passport_data):
        self.full_name = passport_data["full_name"]
        self.birth_date = passport_data["birth_date"]
        self.passport_number = passport_data["passport_number"]
        self.issue_date = passport_data["issue_date"]
        self.issued_by = passport_data["issued_by"]

    def get_passport_data(self):
        return {
            "full_name": self.full_name,
            "birth_date": self.birth_date,
            "passport_number": self.passport_number,
            "issue_date": self.issue_date,
            "issued_by": self.issued_by,
        }

    def display_passport(self):
        data = self.get_passport_data()
        return f"""
┌───────────────────── ПАСПОРТ РБ ─────────────────────┐
│ ФИО: {data['full_name']:<35} │
│ Дата рождения: {data['birth_date']:<28} │
│ Номер паспорта: {data['passport_number']:<27} │
│ Дата выдачи: {data['issue_date']:<29} │
│ Кем выдан: {data['issued_by']:<30} │
└───────────────────────────────────────────────────────┘
        """


class InsuranceSystem:
    def __init__(self, policy_number, company, valid_until):
        self.policy_number = policy_number
        self.company = company
        self.valid_until = valid_until

    def get_insurance_data(self):
        return {
            "policy_number": self.policy_number,
            "company": self.company,
            "valid_until": self.valid_until,
        }

    def check_coverage(self, service_type):
        return service_type in [
            "амбулаторная",
            "стационарная",
            "скорая помощь",
            "стоматология",
        ]

    def display_insurance(self):
        data = self.get_insurance_data()
        return f"""
┌────────────────── МЕДИЦИНСКИЙ ПОЛИС ──────────────────┐
│ Номер полиса: {data['policy_number']:<30} │
│ Страховая компания: {data['company']:<25} │
│ Действителен до: {data['valid_until']:<27} │
└───────────────────────────────────────────────────────┘
        """


class BankCardSystem:
    def __init__(self, card_number, owner_name, expiry_date, initial_balance):
        self.card_number = card_number
        self.owner_name = owner_name
        self.balance = initial_balance
        self.expiry_date = expiry_date
        self.transactions = []

    def get_card_data(self):
        return {
            "card_number": f"**** **** **** {self.card_number[-4:]}",
            "owner": self.owner_name,
            "balance": self.balance,
            "expiry": self.expiry_date,
        }

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"-{amount} руб.")
            return True, f"Снято {amount} руб. Остаток: {self.balance} руб."
        return False, f"Недостаточно средств. Доступно: {self.balance} руб."

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"+{amount} руб.")
        return f"Счет пополнен на {amount} руб. Баланс: {self.balance} руб."

    def display_card(self):
        data = self.get_card_data()
        return f"""
┌──────────────────── БАНКОВСКАЯ КАРТА ─────────────────┐
│ Владелец: {data['owner']:<35} │
│ Номер карты: {data['card_number']:<30} │
│ Срок действия: {data['expiry']:<30} │
│ Баланс: {data['balance']:<20} руб.│
└───────────────────────────────────────────────────────┘
        """


class UniversalCardInterface(ABC):
    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def show_insurance(self):
        pass

    @abstractmethod
    def get_full_info(self):
        pass


class UniversalCard(UniversalCardInterface):
    def __init__(self, passport, insurance, bank_card):
        self._passport = passport
        self._insurance = insurance
        self._bank_card = bank_card
        self.card_id = f"УЭК-{hash(self) % 10000:04d}"

    def identify(self):
        print("\n🔍 ИДЕНТИФИКАЦИЯ ЛИЧНОСТИ:")
        passport_data = self._passport.get_passport_data()
        return f"Гражданин: {passport_data['full_name']}, Паспорт: {passport_data['passport_number']}"

    def pay(self, amount):
        print(f"\n💳 ОПЕРАЦИЯ: ПЛАТЕЖ на сумму {amount} руб.")
        success, message = self._bank_card.withdraw(amount)
        if success:
            return f"✅ {message}"
        return f"❌ {message}"

    def show_insurance(self):
        print("\n🏥 МЕДИЦИНСКАЯ СТРАХОВКА:")
        return self._insurance.display_insurance()

    def get_full_info(self):
        info = f"""
╔══════════════════════════════════════════════════════════╗
║           УНИВЕРСАЛЬНАЯ ЭЛЕКТРОННАЯ КАРТА               ║
╠══════════════════════════════════════════════════════════╣
║ ID карты: {self.card_id:<48} ║
╚══════════════════════════════════════════════════════════╝
        """
        return (
            info
            + self._passport.display_passport()
            + self._insurance.display_insurance()
            + self._bank_card.display_card()
        )

    def top_up_balance(self, amount):
        print(f"\n💰 ПОПОЛНЕНИЕ БАЛАНСА: +{amount} руб.")
        return self._bank_card.deposit(amount)

    def check_insurance_coverage(self, service):
        if self._insurance.check_coverage(service):
            return f"✅ Услуга '{service}' покрывается страховкой"
        return f"❌ Услуга '{service}' НЕ покрывается страховкой"


def input_passport_data():
    print("\n📋 ВВОД ПАСПОРТНЫХ ДАННЫХ:")
    passport_data = {
        "full_name": input("Введите ФИО полностью: "),
        "birth_date": input("Введите дату рождения (ДД.ММ.ГГГГ): "),
        "passport_number": input("Введите номер паспорта (серия номер): "),
        "issue_date": input("Введите дату выдачи (ДД.ММ.ГГГГ): "),
        "issued_by": input("Введите кем выдан паспорт: "),
    }
    return PassportSystem(passport_data)


def input_insurance_data():
    print("\n🏥 ВВОД ДАННЫХ СТРАХОВОГО ПОЛИСА:")
    policy_number = input("Введите номер полиса: ")
    company = input("Введите страховую компанию: ")
    valid_until = input("Введите срок действия до (ДД.ММ.ГГГГ): ")

    return InsuranceSystem(policy_number, company, valid_until)


def input_bank_card_data():
    print("\n💳 ВВОД ДАННЫХ БАНКОВСКОЙ КАРТЫ:")
    card_number = input("Введите номер карты (16 цифр): ")
    owner_name = input("Введите имя владельца (латиницей): ")
    expiry_date = input("Введите срок действия (ММ/ГГ): ")

    while True:
        try:
            initial_balance = float(input("Введите начальный баланс (руб.): "))
            break
        except ValueError:
            print("Ошибка: введите число")

    return BankCardSystem(card_number, owner_name, expiry_date, initial_balance)


def input_all_data():
    passport = input_passport_data()
    insurance = input_insurance_data()
    bank_card = input_bank_card_data()
    return passport, insurance, bank_card


def create_card(passport, insurance, bank_card):
    card = UniversalCard(passport, insurance, bank_card)
    print("\n" + "=" * 80)
    print("✅ УНИВЕРСАЛЬНАЯ КАРТА УСПЕШНО СОЗДАНА!")
    print("=" * 80)
    print(card.get_full_info())
    return card


def show_menu():
    print("\n" + "=" * 50)
    print("ДОСТУПНЫЕ ОПЕРАЦИИ С КАРТОЙ:")
    print("1. Идентификация личности")
    print("2. Показать медицинскую страховку")
    print("3. Проверить покрытие страховки")
    print("4. Совершить платеж")
    print("5. Пополнить баланс карты")
    print("6. Показать полную информацию")
    print("0. Выход")


def process_menu_choice(card, choice):
    if choice == "1":
        print(card.identify())
    elif choice == "2":
        print(card.show_insurance())
    elif choice == "3":
        service = input("Введите тип медицинской услуги: ")
        print(card.check_insurance_coverage(service))
    elif choice == "4":
        try:
            amount = float(input("Введите сумму платежа: "))
            print(card.pay(amount))
        except ValueError:
            print("Ошибка: введите число")
    elif choice == "5":
        try:
            amount = float(input("Введите сумму пополнения: "))
            print(card.top_up_balance(amount))
        except ValueError:
            print("Ошибка: введите число")
    elif choice == "6":
        print(card.get_full_info())
    elif choice == "0":
        return False
    else:
        print("Неверный выбор. Попробуйте снова.")
    return True


def run_card_menu(card):
    while True:
        show_menu()
        choice = input("\nВыберите операцию (0-6): ")
        if not process_menu_choice(card, choice):
            break


def main():
    print("=" * 80)
    print("ПРОГРАММА: УНИВЕРСАЛЬНАЯ ЭЛЕКТРОННАЯ КАРТА")
    print("=" * 80)
    print("\nДобро пожаловать в систему оформления универсальной карты!")

    print("\n" + "=" * 80)
    print("ЭТАП 1: ЗАПОЛНЕНИЕ ДАННЫХ ДЛЯ КАРТЫ")
    print("=" * 80)

    passport, insurance, bank_card = input_all_data()
    card = create_card(passport, insurance, bank_card)
    run_card_menu(card)

    print("\n" + "=" * 80)
    print("СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ УНИВЕРСАЛЬНОЙ КАРТЫ!")
    print("=" * 80)


if __name__ == "__main__":
    main()
