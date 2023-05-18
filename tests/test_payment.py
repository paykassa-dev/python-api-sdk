from unittest import TestCase

from paykassa.struct import System, Currency
from paykassa.dto import CheckBalanceRequest, MakePaymentRequest
from paykassa.payment import PaymentApi


class PaymentApiMock(PaymentApi):
    def _make_request(self, endpoint: str, request: dict) -> dict:
        if endpoint == "api_get_shop_balance":
            return {
                "error": False,
                "message": "Balance store successfully received.",
                "data": {
                    "binancesmartchain_bep20_ada": "1100300.003423400",
                    "bitcoin_btc": "6.19148781",
                }
            }

        if endpoint == "api_payment":
            return {
                "error": False,
                "message": "Data has been successfully received.",
                "data": {
                    "shop_id": "123",
                    "transaction": "130236",
                    "txid": "70d6dc6841782c6efd8deac4b44d9cc3338fda7af38043dd47d7cbad7e84d5dd",
                    "amount": "1.01",
                    "amount_pay": "1.0306",
                    "system": "BitCoin",
                    "currency": "BTC",
                    "number": "3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE",
                    "shop_commission_percent": "1.5",
                    "shop_commission_amount": "1.0",
                    "paid_commission": "shop"
                }
            }

        return {
            "error": True,
            "message": "Unexpected error",
            "data": {},
        }


class TestPaymentApi(TestCase):
    def setUp(self) -> None:
        self.client = PaymentApiMock("1", "test")

    def test_check_balance(self):
        response = self.client.check_balance(CheckBalanceRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Balance store successfully received.", response.get_message())

        self.assertEqual("6.19148781", response.get_balance(System.BITCOIN, Currency.BTC))
        self.assertEqual("1100300.003423400", response.get_balance(System.BINANCESMARTCHAIN_BEP20, Currency.ADA))

    def test_make_payment(self):
        response = self.client.make_payment(MakePaymentRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Data has been successfully received.", response.get_message())

        self.assertEqual("123", response.get_shop_id())
        self.assertEqual("130236", response.get_transaction())
        self.assertEqual("70d6dc6841782c6efd8deac4b44d9cc3338fda7af38043dd47d7cbad7e84d5dd", response.get_txid())
        self.assertEqual("1.01", response.get_amount())
        self.assertEqual("1.0306", response.get_amount_pay())
        self.assertEqual(System.BITCOIN, response.get_system())
        self.assertEqual(Currency.BTC, response.get_currency())
        self.assertEqual("3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE", response.get_number())
        self.assertEqual("1.5", response.get_shop_commission_percent())
        self.assertEqual("1.0", response.get_shop_commission_amount())
        self.assertEqual("shop", response.get_paid_commission())

