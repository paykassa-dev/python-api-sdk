from enum import Enum


class CommissionPayer(Enum):
    SHOP = "shop"
    CLIENT = "client"


class TransactionPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Currency(Enum):
    USD = "USD"
    RUB = "RUB"
    BTC = "BTC"
    DOGE = "DOGE"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    BCH = "BCH"
    ZEC = "ZEC"
    XRP = "XRP"
    TRX = "TRX"
    XLM = "XLM"
    BNB = "BNB"
    USDT = "USDT"
    BUSD = "BUSD"
    USDC = "USDC"
    ADA = "ADA"
    EOS = "EOS"
    SHIB = "SHIB"
    ETC = "ETC"


class System(Enum):
    BERTY = "7"
    BITCOIN = "11"
    ETHEREUM = "12"
    LITECOIN = "14"
    DOGECOIN = "15"
    DASH = "16"
    BITCOINCASH = "18"
    ZCASH = "19"
    ETHEREUMCLASSIC = "21"
    RIPPLE = "22"
    TRON = "27"
    STELLAR = "28"
    BINANCECOIN = "29"
    TRON_TRC20 = "30"
    BINANCESMARTCHAIN_BEP20 = "31"
    ETHEREUM_ERC20 = "32"
