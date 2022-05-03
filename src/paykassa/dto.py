from paykassa.struct import TransactionPriority, Currency, System, CommissionPayer


class Request(object):
    def normalize(self) -> dict:
        pass


class Response:
    _response_systems = {
        "PerfectMoney": System.PERFECTMONEY,
        "Berty": System.BERTY,
        "BitCoin": System.BITCOIN,
        "Ethereum": System.ETHEREUM,
        "Litecoin": System.BITCOIN,
        "Dogecoin": System.DOGECOIN,
        "Dash": System.DASH,
        "BitcoinCash": System.BITCOINCASH,
        "Zcash": System.ZCASH,
        "Ripple": System.RIPPLE,
        "TRON": System.TRON,
        "Stellar": System.STELLAR,
        "BinanceCoin": System.BINANCECOIN,
        "TRON_TRC20": System.TRON_TRC20,
        "BinanceSmartChain_BEP20": System.BINANCESMARTCHAIN_BEP20,
        "Ethereum_ERC20": System.ETHEREUM_ERC20
    }

    def __init__(self, data: dict):
        self._error = data["error"]
        self._message = data["message"]
        self._data = data["data"]

    def has_error(self) -> bool:
        return self._error

    def get_message(self) -> str:
        return self._message

    def _get_system(self, name: str) -> System:
        if name not in self._response_systems:
            raise KeyError("Unknown system: " + name)

        return self._response_systems[name]


class CheckBalanceRequest(Request):
    def __init__(self):
        self.__shop = ""

    def set_shop(self, shop: str):
        self.__shop = shop
        return self

    def normalize(self) -> dict:
        return {
            "shop": self.__shop
        }


class CheckBalanceResponse(Response):
    def get_balance(self, system: System, currency: Currency) -> float:
        if self.__get_system_currency_pair(currency, system) not in self._data:
            raise KeyError("Can't get a balance by system %s and currency %s" % (system.name, currency.name))

        return float(self._data[self.__get_system_currency_pair(currency, system)])

    @staticmethod
    def __get_system_currency_pair(currency, system):
        return system.name.lower() + '_' + currency.name.lower()


class MakePaymentRequest(Request):
    def __init__(self):
        self.__test = False
        self.__priority = TransactionPriority.MEDIUM
        self.__tag = 0
        self.__number = ""
        self.__paid_commission = CommissionPayer.SHOP
        self.__system = System.BITCOIN
        self.__currency = Currency.BTC
        self.__shop = ""
        self.__amount = 0.0

    def set_shop(self, shop: str):
        self.__shop = shop
        return self

    def set_amount(self, amount: float):
        self.__amount = amount
        return self

    def set_currency(self, currency: Currency):
        self.__currency = currency
        return self

    def set_system(self, system: System):
        self.__system = system
        return self

    def set_paid_commission(self, paid_commission: CommissionPayer):
        self.__paid_commission = paid_commission
        return self

    def set_number(self, number: str):
        self.__number = number
        return self

    def set_tag(self, tag: int):
        self.__tag = tag
        return self

    def set_priority(self, priority: TransactionPriority):
        self.__priority = priority
        return self

    def set_test(self, test: bool):
        self.__test = test
        return self

    def normalize(self) -> dict:
        return {
            "priority": self.__priority.value,
            "tag": self.__tag,
            "number": self.__number,
            "paid_commission": self.__paid_commission.value,
            "system": self.__system.value,
            "currency": self.__currency.value,
            "shop": self.__shop,
            "amount": self.__amount,
            "test": self.__test,
        }


class MakePaymentResponse(Response):
    def get_shop_id(self) -> str:
        return str(self._data["shop_id"])

    def get_transaction(self) -> str:
        return str(self._data["transaction"])

    def get_txid(self) -> str:
        return str(self._data["txid"])

    def get_amount(self) -> float:
        return float(self._data["amount"])

    def get_amount_pay(self) -> float:
        return float(self._data["amount_pay"])

    def get_system(self) -> System:
        return self._get_system(self._data["system"])

    def get_currency(self) -> Currency:
        return Currency(str(self._data["currency"]))

    def get_number(self) -> str:
        return str(self._data["number"])

    def get_shop_commission_percent(self) -> float:
        return float(self._data["shop_comission_percent"])

    def get_shop_commission_amount(self) -> float:
        return float(self._data["shop_comission_amount"])

    def get_paid_commission(self) -> str:
        return str(self._data["paid_commission"])


class CheckPaymentRequest(Request):
    def __init__(self):
        self.__test = False
        self.__private_hash = ""

    def set_private_hash(self, private_hash: str):
        self.__private_hash = private_hash
        return self

    def set_test(self, test: bool):
        self.__test = test
        return self

    def normalize(self) -> dict:
        return {
            "private_hash": self.__private_hash,
            "test": self.__test,
        }


class CheckPaymentResponse(Response):
    def get_transaction(self) -> int:
        return int(self._data["transaction"])

    def get_shop_id(self) -> int:
        return int(self._data["shop_id"])

    def get_order_id(self) -> str:
        return str(self._data["order_id"])

    def get_amount(self) -> float:
        return float(self._data["amount"])

    def get_currency(self) -> Currency:
        return Currency(self._data["currency"])

    def get_system(self) -> System:
        return self._get_system(self._data["system"])

    def get_address(self) -> str:
        return str(self._data["address"])

    def get_tag(self) -> str:
        return str(self._data["tag"]) if "tag" in self._data else ""

    def get_hash(self) -> str:
        return str(self._data["hash"])

    def is_partial(self) -> bool:
        return True if self._data["partial"] == "yes" else False


class CheckTransactionRequest(Request):
    def __init__(self):
        self.__test = False
        self.__private_hash = ""

    def set_private_hash(self, private_hash: str):
        self.__private_hash = private_hash
        return self

    def set_test(self, test: bool):
        self.__test = test
        return self

    def normalize(self) -> dict:
        return {
            "private_hash": self.__private_hash,
            "test": self.__test,
        }


class CheckTransactionResponse(Response):
    def get_transaction(self) -> int:
        return int(self._data["transaction"])

    def get_txid(self) -> str:
        return str(self._data["txid"])

    def get_shop_id(self) -> int:
        return int(self._data["shop_id"])

    def get_order_id(self) -> str:
        return str(self._data["order_id"])

    def get_amount(self) -> float:
        return float(self._data["amount"])

    def get_fee(self) -> float:
        return float(self._data["fee"])

    def get_currency(self) -> Currency:
        return Currency(self._data["currency"])

    def get_system(self) -> System:
        return self._get_system(self._data["system"])

    def get_address_from(self) -> str:
        return str(self._data["address_from"])

    def get_address(self) -> str:
        return str(self._data["address"])

    def get_tag(self) -> str:
        return str(self._data["tag"]) if "tag" in self._data else ""

    def get_confirmations(self) -> int:
        return int(self._data["confirmations"])

    def get_required_confirmations(self) -> int:
        return int(self._data["required_confirmations"])

    def get_status(self) -> str:
        return str(self._data["status"])

    def get_date_update(self) -> str:
        return str(self._data["date_update"])

    def get_explorer_address_link(self) -> str:
        return str(self._data["explorer_address_link"])

    def get_explorer_transaction_link(self) -> str:
        return str(self._data["explorer_transaction_link"])


class GenerateAddressRequest(Request):
    def __init__(self):
        self.__test = False
        self.__order_id = ""
        self.__amount = 0.0
        self.__currency = Currency.BTC
        self.__system = System.BITCOIN
        self.__comment = ""
        self.__paid_commission = CommissionPayer.SHOP

    def set_order_id(self, order_id: str):
        self.__order_id = order_id
        return self

    def set_amount(self, amount: float):
        self.__amount = amount
        return self

    def set_currency(self, currency: Currency):
        self.__currency = currency
        return self

    def set_system(self, system: System):
        self.__system = system
        return self

    def set_comment(self, comment: str):
        self.__comment = comment
        return self

    def set_paid_commission(self, paid_commission: CommissionPayer):
        self.__paid_commission = paid_commission
        return self

    def set_test(self, test: bool):
        self.__test = test
        return self

    def normalize(self) -> dict:
        return {
            "order_id": self.__order_id,
            "amount": self.__amount,
            "currency": self.__currency.value,
            "system": self.__system.value,
            "comment": self.__comment,
            "paid_commission": self.__paid_commission.value,
            "phone": False,
            "test": self.__test,
        }


class GenerateAddressResponse(Response):
    def get_invoice(self) -> int:
        return int(self._data["invoice"])

    def get_status(self) -> str:
        return str(self._data["status"])

    def get_order_id(self) -> str:
        return str(self._data["order_id"])

    def get_wallet(self) -> str:
        return str(self._data["wallet"])

    def get_amount(self) -> float:
        return float(self._data["amount"])

    def get_system(self) -> System:
        return self._get_system(self._data["system"])

    def get_currency(self) -> Currency:
        return Currency(self._data["currency"])

    def get_url(self) -> str:
        return str(self._data["url"])

    def get_tag(self) -> str:
        return str(self._data["tag"]) if "tag" in self._data else ""


class GetPaymentUrlRequest(Request):
    def __init__(self):
        self.__test = False
        self.__order_id = ""
        self.__amount = 0.0
        self.__currency = Currency.USD
        self.__system = System.PERFECTMONEY
        self.__comment = ""
        self.__paid_commission = CommissionPayer.SHOP

    def set_order_id(self, order_id: str):
        self.__order_id = order_id
        return self

    def set_amount(self, amount: float):
        self.__amount = amount
        return self

    def set_currency(self, currency: Currency):
        self.__currency = currency
        return self

    def set_system(self, system: System):
        self.__system = system
        return self

    def set_comment(self, comment: str):
        self.__comment = comment
        return self

    def set_paid_commission(self, paid_commission: CommissionPayer):
        self.__paid_commission = paid_commission
        return self

    def set_test(self, test: bool):
        self.__test = test
        return self

    def normalize(self) -> dict:
        return {
            "order_id": self.__order_id,
            "amount": self.__amount,
            "currency": self.__currency.value,
            "system": self.__system.value,
            "comment": self.__comment,
            "paid_commission": self.__paid_commission.value,
            "phone": False,
            "test": self.__test,
        }


class GetPaymentUrlResponse(Response):
    def get_url(self) -> str:
        return str(self._data["url"])

    def get_method(self) -> str:
        return str(self._data["method"])

    def get_params(self) -> dict:
        return self._data["params"]
