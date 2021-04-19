from __future__ import annotations

from enum import Enum
from typing import Dict, Union
from dataclasses import dataclass


class Currency(Enum):
    USD = "usd"
    CHF = "chf"


@dataclass(eq=True, frozen=True)
class Money:
    amount: float
    currency: Currency

    def plus(self, added: Money) -> Sum:
        return Sum(self, added)

    def times(self, multiplier: int) -> Money:
        return Money(self.amount * multiplier, self.currency)

    def reduced(self, bank: Bank, currency: Currency) -> Money:
        rate = bank.rate(self.currency, currency)
        return Money(self.amount / rate, currency)

    @staticmethod
    def dollar(amount: int) -> Money:
        return Money(amount, Currency.USD)

    @staticmethod
    def franc(amount: int) -> Money:
        return Money(amount, Currency.CHF)


@dataclass
class Sum:
    augend: Money
    addend: Money

    def reduced(self, bank: Bank, currency: Currency) -> Money:
        amount = self.augend.amount + self.addend.amount
        return Money(amount, currency)


@dataclass(eq=True, frozen=True, unsafe_hash=True)
class Pair:
    _from: Currency
    _to: Currency


class Bank:
    rates: Dict[Pair, int] = {}

    def reduced(self, source: Union[Sum, Money], currency: Currency) -> Money:
        return source.reduced(self, currency)

    def addRate(self, _from: Currency, _to: Currency, rate: int):
        self.rates[Pair(_from=_from, _to=_to)] = rate

    def rate(self, _from: Currency, _to: Currency) -> int:
        if _from == _to:
            return 1

        return self.rates[Pair(_from=_from, _to=_to)]
