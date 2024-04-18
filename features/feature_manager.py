from features.auth_feature import AuthFeature
from features.account_transfer_feature import AccountTransferFeature


class Features:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.auth_feature = AuthFeature()
            cls._instance.account_transfer_feature = AccountTransferFeature()
        return cls._instance
