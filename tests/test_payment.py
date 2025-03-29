from unittest import TestCase

from paykassa.struct import System, Currency
from paykassa.dto import CheckBalanceRequest, MakePaymentRequest, GetTxidsOfInvoicesRequest
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
        elif endpoint == "api_get_shop_txids":
            return {
                "error": False,
                "message": "Ok",
                "data": {
                    "111111111": [
                        "111111111555555555666666667777777788888888889999999"
                    ],
                    "222222222": [
                        "222222222555555555666666667777777788888888889999999"
                    ],
                    "3333333333": [
                        "3333333333555555555666666667777777788888888889999999"
                    ]
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


    def test_get_txids_by_invoices(self):
        response = self.client.get_txids_by_invoices(GetTxidsOfInvoicesRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Ok", response.get_message())

        self.assertEqual([
                        "111111111555555555666666667777777788888888889999999"
                    ], response.get_txids_of_invoice("111111111"))
        self.assertEqual([
                        "222222222555555555666666667777777788888888889999999"
                    ], response.get_txids_of_invoice("222222222"))

        self.assertEqual([
                        "3333333333555555555666666667777777788888888889999999"
                    ], response.get_txids_of_invoice("3333333333"))

        with self.assertRaises(KeyError) as context:
            response.get_txids_of_invoice("4444444444")

        self.assertEqual(
            context.exception.args[0],
            "The txids of the invoice 4444444444 is not found"
        )
