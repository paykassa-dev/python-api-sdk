import requests

from paykassa.dto import CheckBalanceRequest, CheckBalanceResponse, MakePaymentRequest, MakePaymentResponse


class PaymentApiInterface(object):
    def check_balance(self, request: CheckBalanceRequest) -> CheckBalanceResponse:
        pass

    def make_payment(self, request: MakePaymentRequest) -> MakePaymentResponse:
        pass


class PaymentApiBase(PaymentApiInterface):
    BASE_URL = "https://paykassa.app/api/"
    API_VERSION = 0.5

    def __init__(self, api_id: int, api_key: str):
        self._api_id = api_id
        self._api_key = api_key

    def set_api_id(self, api_id: str) -> 'PaymentApiBase':
        self._api_id = api_id
        return self

    def set_api_key(self, api_key: str) -> 'PaymentApiBase':
        self._api_key = api_key
        return self

    def _make_request(self, endpoint: str, request: dict) -> dict:
        try:
            self.__set_method_data(endpoint, request)
            return requests.post(self.__get_api_url(), request).json()
        except Exception as e:
            return PaymentApiBase.__get_error_response(e)

    @staticmethod
    def __get_error_response(e: Exception) -> dict:
        return {
            "error": True,
            "message": str(e),
            "data": {},
        }

    def __get_api_url(self):
        return self.BASE_URL + str(self.API_VERSION) + "/index.php"

    def __set_method_data(self, endpoint: str, request: dict):
        request["func"] = endpoint
        request["api_id"] = self._api_id
        request["api_key"] = self._api_key


class PaymentApi(PaymentApiBase):
    def __init__(self, api_id: int, api_key: str):
        super(PaymentApi, self).__init__(api_id, api_key)

    # see https://paykassa.pro/docs/#api-API-api_get_shop_balance
    def check_balance(self, request: CheckBalanceRequest) -> CheckBalanceResponse:
        return CheckBalanceResponse(self._make_request("api_get_shop_balance", request.normalize()))

    # see https://paykassa.pro/docs/#api-API-api_payment
    def make_payment(self, request: MakePaymentRequest) -> MakePaymentResponse:
        return MakePaymentResponse(self._make_request('api_payment', request.normalize()))
