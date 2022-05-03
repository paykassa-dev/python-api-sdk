import requests

from paykassa.dto import CheckPaymentRequest, CheckPaymentResponse, CheckTransactionRequest, CheckTransactionResponse, \
    GenerateAddressRequest, GenerateAddressResponse, GetPaymentUrlRequest, GetPaymentUrlResponse


class MerchantApiInterface(object):
    def check_payment(self, request: CheckPaymentRequest) -> CheckPaymentResponse:
        pass

    def check_transaction(self, request: CheckTransactionRequest) -> CheckTransactionResponse:
        pass

    def generate_address(self, request: GenerateAddressRequest) -> GenerateAddressResponse:
        pass

    def get_payment_url(self, request: GetPaymentUrlRequest) -> GetPaymentUrlResponse:
        pass


class MerchantApiBase(MerchantApiInterface):
    BASE_URL = "https://paykassa.app/sci/"
    API_VERSION = 0.4

    def __init__(self, api_id: int, api_key: str):
        self._sci_id = api_id
        self._sci_key = api_key

    def set_sci_id(self, api_id: str):
        self._sci_id = api_id
        return self

    def set_sci_key(self, api_key: str):
        self._sci_key = api_key
        return self

    def _make_request(self, endpoint: str, request: dict) -> dict:
        try:
            self.__set_method_data(endpoint, request)
            return requests.post(self.__get_api_url(), request).json()
        except Exception as e:
            return MerchantApiBase.__get_error_response(e)

    def __get_api_url(self):
        return self.BASE_URL + str(self.API_VERSION) + "/index.php"

    def __set_method_data(self, endpoint: str, request: dict):
        request["func"] = endpoint
        request["sci_id"] = self._sci_id
        request["sci_key"] = self._sci_key

    @staticmethod
    def __get_error_response(e: Exception) -> dict:
        return {
            "error": True,
            "message": str(e),
            "data": {},
        }


class MerchantApi(MerchantApiBase):
    def __init__(self, sci_id: int, sci_key: str):
        super(MerchantApi, self).__init__(sci_id, sci_key)

    # see https://paykassa.pro/docs/#api-SCI-sci_confirm_order
    def check_payment(self, request: CheckPaymentRequest) -> CheckPaymentResponse:
        return CheckPaymentResponse(self._make_request("sci_confirm_order", request.normalize()))

    # see https://paykassa.pro/docs/#api-SCI-sci_confirm_transaction_notification
    def check_transaction(self, request: CheckTransactionRequest) -> CheckTransactionResponse:
        return CheckTransactionResponse(self._make_request("sci_confirm_transaction_notification", request.normalize()))

    # see https://paykassa.pro/docs/#api-SCI-sci_create_order_get_data
    def generate_address(self, request: GenerateAddressRequest) -> GenerateAddressResponse:
        return GenerateAddressResponse(self._make_request("sci_create_order_get_data", request.normalize()))

    # see https://paykassa.pro/docs/#api-SCI-sci_create_order
    def get_payment_url(self, request: GetPaymentUrlRequest) -> GetPaymentUrlResponse:
        return GetPaymentUrlResponse(self._make_request("sci_create_order", request.normalize()))
