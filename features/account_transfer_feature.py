from lib.api_service_provider.account.account_api_service import account_api_service
from lib.data_provider.models.user import User


class AccountTransferFeature:

    def set_customer_id(self, user) -> None:
        """ set customer ID"""
        user.customerId = account_api_service.overview()

    def set_customer_accounts(self, user: User) -> None:
        """ set customer accounts """
        user.accounts = account_api_service.accounts(user.customerId)

    def validate_account_balance(self, user: User, transfer_percentage: int) -> bool:
        """ Validate the balances after transfer is done."""
        self.validate_min_account_req(user)
        from_account, to_account = user.accounts[0], user.accounts[1]
        latest_account_data = account_api_service.accounts(user.customerId)
        amount_change = (transfer_percentage/100) * from_account["balance"]
        from_account["balance"] -= amount_change
        to_account["balance"] += amount_change

        from_updated, to_updated = False, False
        for account in latest_account_data:
            if account["id"] == from_account["id"]:
                if account["balance"] == from_account["balance"]:
                    from_updated = True
            if account["id"] == to_account["id"]:
                if account["balance"] == to_account["balance"]:
                    to_updated = True

        return from_updated, to_updated

    def create_new_account_if_required(self, user: User, account_type: int) -> bool:
        """ Creates a new account if customer only has one account"""
        prev_account_count = len(user.accounts)
        if prev_account_count <= 1:
            from_account = user.accounts[0]["id"]
            new_account = account_api_service.create_account(user.customerId, account_type.value, from_account)
            if new_account != None:
                user.accounts = account_api_service.accounts(user.customerId)
            else:
                raise Exception("Unable to fetch customer accounts")
            if len(account_api_service.accounts(user.customerId)) != prev_account_count + 1:
                return False
        return True

    def transfer_funds(self, user: User, amount_percentage: int)-> bool:
        """Transfer Funds between accounts based on percentage"""
        self.validate_min_account_req(user)
        from_account, to_account = user.accounts[0], user.accounts[1]
        amount = (amount_percentage/100) * from_account["balance"]

        data = account_api_service.transfer(from_account['id'], to_account['id'], amount)
        if f"Successfully transferred ${amount} from account #{from_account['id']} to " \
           f"account #{to_account['id']}" in data:
            return True
        return False

    def validate_min_account_req(self, user: User):
        prev_account_count = len(user.accounts)
        if prev_account_count <= 1:
            raise Exception("Min 2 accounts required.")



