from __future__ import annotations

from typing import Optional


class Money:
    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, obj: Money) -> bool:
        if not isinstance(obj, Money):
            raise TypeError()

        is_same_class = self.__class__ == obj.__class__
        is_same_amount = self._amount == obj._amount
        return is_same_amount and is_same_class

    def times(self, multiplier: int) -> Money:
        raise NotImplementedError()

    def currency(self) -> str:
        return self._currency

    @staticmethod
    def dollar(amount: int) -> Dollar:
        return Dollar(amount, "USD")

    @staticmethod
    def franc(amount: int) -> Franc:
        return Franc(amount, "CHF")


class Dollar(Money):
    def times(self, multiplier: int) -> Dollar:
        return Money.dollar(self._amount * multiplier)


class Franc(Money):
    def times(self, multiplier: int) -> Franc:
        return Money.franc(self._amount * multiplier)
