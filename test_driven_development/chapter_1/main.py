from __future__ import annotations

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Money:
    amount: int
    currency: str

    def times(self, multiplier: int) -> Money:
        return Money(self.amount * multiplier, self.currency)

    @staticmethod
    def dollar(amount: int) -> Money:
        return Money(amount, "USD")

    @staticmethod
    def franc(amount: int) -> Money:
        return Money(amount, "CHF")
