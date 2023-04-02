from httpx import AsyncClient

from paykassa.dto import CheckBalanceRequest, CheckBalanceResponse, MakePaymentRequest, MakePaymentResponse


class PaymentApiInterface(object):
    async def check_balance(self, request: CheckBalanceRequest) -> CheckBalanceResponse:
        raise NotImplementedError

    async def make_payment(self, request: MakePaymentRequest) -> MakePaymentResponse:
        raise NotImplementedError


class PaymentApiBase(PaymentApiInterface):
    BASE_URL = "https://paykassa.app/api/"
    API_VERSION = 0.5

    def __init__(self, api_id: int, api_key: str):
        self._api_id = api_id
        self._api_key = api_key
        self._client = AsyncClient()

    def set_api_id(self, api_id: int) -> 'PaymentApiBase':
        self._api_id = api_id
        return self

    def set_api_key(self, api_key: str) -> 'PaymentApiBase':
        self._api_key = api_key
        return self

    async def _make_request(self, endpoint: str, request: dict) -> dict:
        try:
            self.__set_method_data(endpoint, request)
            return (await self._client.post(self.__get_api_url(), json=request)).json()
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
    async def check_balance(self, request: CheckBalanceRequest) -> CheckBalanceResponse:
        response = await self._make_request("api_get_shop_balance", request.normalize())
        return CheckBalanceResponse(response)

    # see https://paykassa.pro/docs/#api-API-api_payment
    async def make_payment(self, request: MakePaymentRequest) -> MakePaymentResponse:
        response = await self._make_request('api_payment', request.normalize())
        return MakePaymentResponse(response)
