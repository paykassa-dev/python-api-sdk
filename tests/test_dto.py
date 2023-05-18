from unittest import TestCase

from paykassa.struct import Currency, System, TransactionPriority, CommissionPayer
from paykassa.dto import CheckBalanceRequest, MakePaymentRequest, CheckPaymentRequest, CheckTransactionRequest, \
    GenerateAddressRequest, GetPaymentUrlRequest


class TestCheckBalanceRequest(TestCase):
    def test_normalize(self):
        request = CheckBalanceRequest() \
            .set_shop_id("123")

        self.assertDictEqual({
            "shop_id": "123"
        }, request.normalize())


class TestMakePaymentRequest(TestCase):
    def test_normalize(self):
        request = MakePaymentRequest() \
            .set_shop_id("123") \
            .set_tag(594) \
            .set_amount(1123.0003233) \
            .set_number("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") \
            .set_priority(TransactionPriority.HIGH) \
            .set_system(System.BITCOIN) \
            .set_currency(Currency.BTC) \
            .set_paid_commission(CommissionPayer.CLIENT) \
            .set_test(True)

        self.assertDictEqual({
            "shop_id": "123",
            "amount": 1123.0003233,
            "currency": "BTC",
            "system": "11",
            "paid_commission": "client",
            "number": "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
            "tag": 594,
            "priority": "high",
            "test": True,
        }, request.normalize())


class TestCheckPaymentRequest(TestCase):
    def test_normalize(self):
        request = CheckPaymentRequest() \
            .set_private_hash("851b7ac0d8bd3e31598b36e564423b4598b15e2f020c1c25fb093ab0b80ec04a") \
            .set_test(True)

        self.assertDictEqual({
            "private_hash": "851b7ac0d8bd3e31598b36e564423b4598b15e2f020c1c25fb093ab0b80ec04a",
            "test": True,
        }, request.normalize())


class TestCheckTransactionRequest(TestCase):
    def test_normalize(self):
        request = CheckTransactionRequest() \
            .set_private_hash("851b7ac0d8bd3e31598b36e564423b4598b15e2f020c1c25fb093ab0b80ec04a") \
            .set_test(True)

        self.assertDictEqual({
            "private_hash": "851b7ac0d8bd3e31598b36e564423b4598b15e2f020c1c25fb093ab0b80ec04a",
            "test": True,
        }, request.normalize())


class TestGenerateAddressRequest(TestCase):
    def test_normalize(self):
        request = GenerateAddressRequest() \
            .set_order_id("order_id") \
            .set_amount("123123.4506456") \
            .set_currency(Currency.BTC) \
            .set_system(System.DOGECOIN) \
            .set_comment("") \
            .set_paid_commission(CommissionPayer.CLIENT) \
            .set_test(True)

        self.assertDictEqual({
            "order_id": "order_id",
            "amount": "123123.4506456",
            "currency": "BTC",
            "system": "15",
            "comment": "",
            "phone": False,
            "paid_commission": "client",
            "test": True,
        }, request.normalize())


class TestGetPaymentUrlRequest(TestCase):
    def test_normalize(self):
        request = GetPaymentUrlRequest() \
            .set_order_id("order_id") \
            .set_amount("123.45") \
            .set_currency(Currency.USDT) \
            .set_system(System.TRON_TRC20) \
            .set_comment("TEST") \
            .set_paid_commission(CommissionPayer.SHOP) \
            .set_test(True)

        self.assertDictEqual({
            "order_id": "order_id",
            "amount": "123.45",
            "currency": "USDT",
            "system": "30",
            "comment": "TEST",
            "phone": False,
            "paid_commission": "shop",
            "test": True,
        }, request.normalize())
