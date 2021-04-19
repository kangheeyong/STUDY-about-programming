import unittest

from .main import Money, Bank, Currency, Sum


class TestCase(unittest.TestCase):
    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_franc_multiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10), five.times(2))
        self.assertEqual(Money.franc(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5) == Money.dollar(5))
        self.assertFalse(Money.dollar(5) == Money.dollar(6))
        self.assertFalse(Money.franc(5) == Money.dollar(5))

    def test_currency(self):
        self.assertEqual(Currency.USD, Money.dollar(1).currency)
        self.assertEqual(Currency.CHF, Money.franc(1).currency)

    def test_simpe_addition(self):
        five = Money.dollar(5)
        _sum = five.plus(five)
        bank = Bank()
        reduced = bank.reduced(_sum, Currency.USD)
        self.assertEqual(Money.dollar(10), reduced)

    def test_plus_returns_sum(self):
        five = Money.dollar(5)
        _sum = five.plus(five)
        self.assertEqual(five, _sum.augend)
        self.assertEqual(five, _sum.addend)

    def test_reduce_sum(self):
        _sum = Sum(Money.franc(5), Money.franc(2))
        bank = Bank()
        reduced = bank.reduced(_sum, Currency.USD)
        self.assertEqual(Money.dollar(7), reduced)

    def test_reduce_money(self):
        bank = Bank()
        reduced = bank.reduced(Money.dollar(1), Currency.USD)
        self.assertEqual(Money.dollar(1), reduced)

    def test_reduce_money_different_curruncy(self):
        bank = Bank()
        bank.addRate(Currency.CHF, Currency.USD, 2)
        result = bank.reduced(Money.franc(2), Currency.USD)
        self.assertEqual(Money.dollar(1), result)

    def test_identity_rate(self):
        self.assertEqual(1, Bank().rate(Currency.USD, Currency.USD))


if __name__ == "__main__":
    unittest.main()
