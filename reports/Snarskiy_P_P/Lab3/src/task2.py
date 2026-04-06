"""Facade universal card"""


class Passport:
    """Passport class"""
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def get_info(self):
        """All passport info"""
        return f"Passport: {self.name}, №{self.number}"

    def get_number(self):
        """Show number"""
        return f"Passport №{self.number}"


class Insurance:
    """Insurance class"""
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.valid_time = 365

    def get_number(self):
        """Insurance number"""
        return f"Insurance policy: №{self.policy_number}"

    def get_time(self):
        """Insurance time"""
        return f"Days till next insurance: {self.valid_time}"


class BankCard:
    """Bank card class"""
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        """Pay money"""
        if amount <= self.balance:
            self.balance -= amount
            return f"Payment successful. Remaining balance: {self.balance}"
        return "Not enough funds"

    def get_balance(self):
        """Bank balance"""
        return f"Balance: {self.balance}"


class UniversalCard:
    """Facade universal card class"""
    def __init__(self, name, passport_number, policy_number, balance):
        self.passport = Passport(name, passport_number)
        self.insurance = Insurance(policy_number)
        self.bank = BankCard(balance)

    def show_all_info(self):
        """Show all info"""
        return "\n".join(
            [
                self.passport.get_info(),
                self.insurance.get_number(),
                self.bank.get_balance(),
            ]
        )

    def pay(self, amount):
        """Pay money"""
        return self.bank.pay(amount)


if __name__ == "__main__":
    card = UniversalCard("Ivan Ivanov", "1234 567890", "POL-001", 1000)

    print(card.show_all_info())
    print(card.pay(200))
