from unittest import TestCase

from paykassa.struct import Currency, System
from paykassa.dto import CheckPaymentRequest, CheckTransactionRequest, GenerateAddressRequest, GetPaymentUrlRequest
from paykassa.merchant import MerchantApi


class MerchantApiMock(MerchantApi):
    def _make_request(self, endpoint: str, request: dict) -> dict:
        if endpoint == "sci_confirm_order":
            return {
                "error": False,
                "message": "Payment successfully verified",
                "data": {
                    "transaction": "96401",
                    "shop_id": "123",
                    "order_id": "12345",
                    "amount": "1.01",
                    "currency": "BTC",
                    "system": "BitCoin",
                    "address": "3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE",
                    "tag": "",
                    "hash": "ba276492c1c8ff5bfad7ea46463aca85d9c447ee940aceeb71e4a726d89458cd",
                    "partial": "no"
                }
            }

        if endpoint == "sci_confirm_transaction_notification":
            return {
                "error": False,
                "message": "Ok",
                "data": {
                    "transaction": "2431038",
                    "txid": "e2be8b51ad0ccbae2a2433f8c940035ce97903c7de1a1cefa1db40cc1cabb0e5",
                    "shop_id": "138",
                    "order_id": "order 1",
                    "amount": "1.00000000",
                    "fee": "0.00000000",
                    "currency": "DOGE",
                    "system": "Dogecoin",
                    "address_from": "",
                    "address": "DKpzDZuFoTpPpnpsMro8NBtmDz8rinCjqp",
                    "tag": "",
                    "confirmations": 0,
                    "required_confirmations": 3,
                    "status": "no",
                    "static": "yes",
                    "date_update": "2020-07-23 15:06:58",
                    "explorer_address_link": "https://explorer.paykassa.pro/address/dogecoin-doge/DKpzDZuFoTpPpnpsMro8NBtmDz8rinCjqp",
                    "explorer_transaction_link": "https://explorer.paykassa.pro/transaction/dogecoin-doge/e2be8b51ad0ccbae2a2433f8c940035ce97903c7de1a1cefa1db40cc1cabb0e5"
                }}

        if endpoint == "sci_create_order_get_data":
            return {
                "error": False,
                "message": "Data has been successfully received.",
                "data": {
                    "invoice_id": "579205",
                    "order_id": "12345",
                    "wallet": "3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE",
                    "amount": "1.03030000",
                    "system": "BitCoin",
                    "currency": "BTC",
                    "url": "https://crypto.paykassa.pro/sci/index.php?hash=ba276492c1c8ff5bfad7ea46463aca85d9c447ee940aceeb71e4a726d89458cd",
                    "tag": False
                }
            }

        if endpoint == "sci_create_order":
            return {
                "error": False,
                "message": "The account is successfully billed",
                "data": {
                    "url": "https://paykassa.app/sci/redir_test.php?hash=9ef8b443c9c73116e6f363382d3d285610a0314b7c9693901561a472d3934072",
                    "method": "GET",
                    "params": {
                        "hash": "9ef8b443c9c73116e6f363382d3d285610a0314b7c9693901561a472d3934072"
                    }
                }
            }

        return {
            "error": True,
            "message": "Unexpected error",
            "data": {},
        }


class TestMerchantApi(TestCase):
    def setUp(self) -> None:
        self.client = MerchantApiMock("1", "test")

    def test_check_payment(self):
        response = self.client.check_payment(CheckPaymentRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Payment successfully verified", response.get_message())

        self.assertEqual("96401", response.get_transaction())
        self.assertEqual("123", response.get_shop_id())
        self.assertEqual("12345", response.get_order_id())
        self.assertEqual("1.01", response.get_amount())
        self.assertEqual(Currency.BTC, response.get_currency())
        self.assertEqual(System.BITCOIN, response.get_system())
        self.assertEqual("3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE", response.get_address())
        self.assertEqual("", response.get_tag())
        self.assertEqual("ba276492c1c8ff5bfad7ea46463aca85d9c447ee940aceeb71e4a726d89458cd", response.get_hash())
        self.assertEqual(False, response.is_partial())

    def test_check_transaction(self):
        response = self.client.check_transaction(CheckTransactionRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Ok", response.get_message())

        self.assertEqual("2431038", response.get_transaction())
        self.assertEqual("e2be8b51ad0ccbae2a2433f8c940035ce97903c7de1a1cefa1db40cc1cabb0e5", response.get_txid())
        self.assertEqual("138", response.get_shop_id())
        self.assertEqual("order 1", response.get_order_id())
        self.assertEqual("1.00000000", response.get_amount())
        self.assertEqual("0.00000000", response.get_fee())
        self.assertEqual(Currency.DOGE, response.get_currency())
        self.assertEqual(System.DOGECOIN, response.get_system())
        self.assertEqual("", response.get_address_from())
        self.assertEqual("DKpzDZuFoTpPpnpsMro8NBtmDz8rinCjqp", response.get_address())
        self.assertEqual("", response.get_tag())
        self.assertEqual(0, response.get_confirmations())
        self.assertEqual(3, response.get_required_confirmations())
        self.assertEqual("no", response.get_status())
        self.assertEqual("2020-07-23 15:06:58", response.get_date_update())
        self.assertEqual("https://explorer.paykassa.pro/address/dogecoin-doge/DKpzDZuFoTpPpnpsMro8NBtmDz8rinCjqp",
                         response.get_explorer_address_link())
        self.assertEqual(
            "https://explorer.paykassa.pro/transaction/dogecoin-doge/e2be8b51ad0ccbae2a2433f8c940035ce97903c7de1a1cefa1db40cc1cabb0e5",
            response.get_explorer_transaction_link())

    def test_generate_address(self):
        response = self.client.generate_address(GenerateAddressRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("Data has been successfully received.", response.get_message())

        self.assertEqual("579205", response.get_invoice_id())
        self.assertEqual("12345", response.get_order_id())
        self.assertEqual("3LaKdUrPfVyZeEVYpZei3HwjqQj5AHHTCE", response.get_wallet())
        self.assertEqual("1.03030000", response.get_amount())
        self.assertEqual(System.BITCOIN, response.get_system())
        self.assertEqual(Currency.BTC, response.get_currency())
        self.assertEqual("https://crypto.paykassa.pro/sci/index.php?hash=ba276492c1c8ff5bfad7ea46463aca85d9c447ee940aceeb71e4a726d89458cd", response.get_url())
        self.assertEqual("False", response.get_tag())

    def test_get_payment_url(self):
        response = self.client.get_payment_url(GetPaymentUrlRequest())

        self.assertFalse(response.has_error())
        self.assertEqual("The account is successfully billed", response.get_message())

        self.assertEqual("https://paykassa.app/sci/redir_test.php?hash=9ef8b443c9c73116e6f363382d3d285610a0314b7c9693901561a472d3934072", response.get_url())
        self.assertEqual("GET", response.get_method())
        self.assertEqual({"hash": "9ef8b443c9c73116e6f363382d3d285610a0314b7c9693901561a472d3934072"}, response.get_params())

