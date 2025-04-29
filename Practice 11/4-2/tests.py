import pytest
import deal
from decimal import Decimal, InvalidOperation
from bank_account import BankAccount


def test_initial_balance_default():
    acc = BankAccount()
    assert acc.balance == Decimal('0')
    assert acc.check_balance() == "Баланс счёта: 0"


def test_initial_balance_from_string():
    acc = BankAccount('10.5')
    assert acc.balance == Decimal('10.5')


def test_invalid_initial_balance():
    with pytest.raises(ValueError):
        BankAccount('not a number')


def test_deposit_positive():
    acc = BankAccount(Decimal('10'))
    msg = acc.deposit('5.25')
    assert acc.balance == Decimal('15.25')
    assert "5.25 средств успешно зачислены" in msg


def test_withdraw_positive():
    acc = BankAccount(Decimal('10.75'))
    msg = acc.withdraw(Decimal('4.75'))
    assert acc.balance == Decimal('6.00')
    assert "4.75 средств успешно сняты" in msg


def test_deposit_negative_amount_raises():
    acc = BankAccount(Decimal('10'))
    with pytest.raises(deal.PreContractError):
        acc.deposit(Decimal('-1'))


def test_withdraw_negative_amount_raises():
    acc = BankAccount(Decimal('10'))
    with pytest.raises(deal.PreContractError):
        acc.withdraw(-5)


def test_withdraw_insufficient_balance_raises():
    acc = BankAccount(Decimal('5'))
    with pytest.raises(deal.PreContractError):
        acc.withdraw(Decimal('10'))


def test_balance_invariant_after_direct_assignment():
    acc = BankAccount(Decimal('5'))
    acc.balance = "not a number"
    with pytest.raises(deal.InvContractError):
        acc.check_balance()


def test_floating_sequence_operations_with_decimal():
    acc = BankAccount(Decimal('0'))
    acc.deposit(Decimal('0.3'))
    acc.withdraw('0.1')
    # баланс должен быть ровно 0.2
    assert acc.balance == Decimal('0.2')
    assert acc.check_balance() == f"Баланс счёта: {acc.balance}"