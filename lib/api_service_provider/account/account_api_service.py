from lib.api_service_provider.api_service import APIService
from lib.api_service_provider.api_constants import APIConstants, REFERERConstants
import re
from lib.logger.logger import logger
from typing import List


class AccountAPIServiceConstants:
    pass


class AccountAPIService(APIService):

    def overview(self) -> None:
        response = self.get(endpoint=APIConstants.OVERVIEW)

        logger.info(f"Request successful - {APIConstants.OVERVIEW}")
        # Extract the number from the URL using regex
        match = re.search(r'services_proxy/bank/customers/" \+ (\d+) \+ "/accounts"', response.text)
        if match:
            customer_id = match.group(1)
            logger.info(f"Extracted number value: {customer_id}")
            return customer_id
        else:
            logger.info(f"Extracted number value: {customer_id}")
            return 0

    def accounts(self, customer_id: str) -> List:
        endpoint = APIConstants.ACCOUNTS.replace("customer_id", customer_id)
        response = self.get(endpoint=endpoint, referer=REFERERConstants.OVERVIEW)
        data = response.json()
        return data

    def create_account(self, customer_id: int , new_account_type: int , from_account: int) -> dict:
        endpoint = APIConstants.CREATE_ACCOUNT
        params = {
            'customerId': customer_id,
            'newAccountType': new_account_type,
            'fromAccountId': from_account
        }
        response = self.post(endpoint=endpoint, origin=APIConstants.ORIGIN, referer=REFERERConstants.OPEN_ACCOUNT,
                             params=params)
        data = response.json()
        return data

    def transfer(self, from_account:int, to_account:int, amount:int) -> str:
        endpoint = APIConstants.TRANSFER

        params = {
            'fromAccountId': from_account,
            'toAccountId': to_account,
            'amount': amount
        }
        response = self.post(endpoint=endpoint, origin=APIConstants.ORIGIN, referer=REFERERConstants.TRANSFER, params=params)
        data = response.text
        return data


account_api_service = AccountAPIService()

