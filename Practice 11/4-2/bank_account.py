import deal
from decimal import Decimal


@deal.inv(lambda self: isinstance(self, Decimal)
          and self.balance >= 0)
class BankAccount:
    balance: Decimal

    @deal.pre(lambda balance: isinstance(balance, (int, float, Decimal))
              and balance >= 0)
    def __init__(self, balance=0):
        self.balance = Decimal(balance)

    @deal.pre(lambda amount: isinstance(amount, (int, float, Decimal))
              and amount >= 0)
    def deposit(self, amount):
        self.balance += Decimal(amount)
        return f"{amount} средств успешно зачислены на счёт."

    @deal.pre(lambda amount: isinstance(amount, (int, float, Decimal))
              and amount >= 0)
    def withdraw(self, amount):
        self.balance -= Decimal(amount)
        return f"{amount} средств успешно сняты с счёта."

    def check_balance(self):
        return f"Баланс счёта: {self.balance}"