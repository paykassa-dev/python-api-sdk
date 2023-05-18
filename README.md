# Paykassa SCI & API

## Installation

```
python -m pip install paykassa-api-sdk
```

## Payment API

### Initialize Client

```python
from paykassa.payment import PaymentApi

client = PaymentApi(api_id, api_key)
```

### Check Balance

```python
from paykassa.dto import CheckBalanceRequest
from paykassa.struct import System, Currency

request = CheckBalanceRequest() \
    .set_shop_id("123")

response = client.check_balance(request)

if not response.has_error():
    print(response.get_balance(System.BITCOIN, Currency.BTC))
    print(response.get_balance(System.ETHEREUM, Currency.ETH))
```

### Make Payment

```python
from paykassa.dto import MakePaymentRequest
from paykassa.struct import System, Currency, CommissionPayer, TransactionPriority 

request = MakePaymentRequest() \
    .set_shop_id("123") \
    .set_amount("1.02") \
    .set_priority(TransactionPriority.MEDIUM) \
    .set_system(System.BITCOIN) \
    .set_currency(Currency.BTC) \
    .set_paid_commission(CommissionPayer.SHOP) \
    .set_number("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy")
 
response = client.make_payment(request)

if not response.has_error():
    print(response.get_transaction())
    print(response.get_paid_commission())
```

## Merchant API

### Initialize Client

```python
from paykassa.merchant import MerchantApi

client = MerchantApi(sci_id, sci_key)
```

### Check Payment (IPN)

```python
from paykassa.dto import CheckPaymentRequest

request = CheckPaymentRequest() \
    .set_private_hash("hash")

response = client.check_payment(request)

if not response.has_error():
    print(response.get_transaction())
```

### Check Transaction (IPN)

```python
from paykassa.dto import CheckTransactionRequest

request = CheckTransactionRequest() \
    .set_private_hash("hash")

response = client.check_transaction(request)

if not response.has_error():
    print(response.get_address_from())
    print(response.get_confirmations())
```

### Generate Address

```python
from paykassa.dto import GenerateAddressRequest
from paykassa.struct import System, Currency, CommissionPayer

request = GenerateAddressRequest() \
    .set_amount("1.123456") \
    .set_currency(Currency.DOGE) \
    .set_system(System.DOGECOIN) \
    .set_comment("test") \
    .set_paid_commission(CommissionPayer.CLIENT)

response = client.generate_address(request)

if not response.has_error():
    print(response.get_amount())
    print(response.get_wallet())
```

### Get Payment Url

```python
from paykassa.dto import GetPaymentUrlRequest
from paykassa.struct import System, Currency, CommissionPayer

request = GetPaymentUrlRequest() \
    .set_amount("110") \
    .set_currency(Currency.USDT) \
    .set_system(System.TRON_TRC20) \
    .set_comment("test") \
    .set_paid_commission(CommissionPayer.CLIENT)

response = client.get_payment_url(request)

if not response.has_error():
    print(response.get_method())
    print(response.get_url())
```

## References
- [Devs Documentation](https://paykassa.pro/en/developers)
- [API Documentation](https://paykassa.pro/docs/)
