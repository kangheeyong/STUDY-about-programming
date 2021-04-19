from __future__ import annotations

from typing import Optional


class Money:
    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, obj: Money) -> bool:
        if not isinstance(obj, Money):
            raise TypeError()

        is_same_currency = self._currency == obj._currency
        is_same_amount = self._amount == obj._amount
        return is_same_amount and is_same_currency

    def __str__(self):
        return f"amount: {self._amount}, currency: {self._currency}"

    def times(self, multiplier: int) -> Money:
        return Money(self._amount * multiplier, self.currency())

    def currency(self) -> str:
        return self._currency

    @staticmethod
    def dollar(amount: int) -> Money:
        return Money(amount, "USD")

    @staticmethod
    def franc(amount: int) -> Money:
        return Money(amount, "CHF")
