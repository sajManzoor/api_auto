from tests.base_case import TestBaseCase
from lib.data_provider.models.user import Account, AccountType


class TestTransferFunds(TestBaseCase):

    def setup_method(self, method):
        super().setup_method(method)
        self.attempt_login(self.data_provider.get_normal_customer())
        self.features.account_transfer_feature.set_customer_id(self.current_user)
        assert self.current_user.customerId != 0, f"Unable to fetch customer ID"
        self.features.account_transfer_feature.set_customer_accounts(self.current_user)
        assert len(self.current_user.accounts) >= 1, f"Unable to fetch customer accounts"
        # create more accounts if needed (for transfer)
        assert self.features.account_transfer_feature.create_new_account_if_required(user=self.current_user, account_type=AccountType.Checking)


    def test_transfer_funds(self):
        assert self.features.account_transfer_feature.transfer_funds(self.current_user, 10), f"Transfer failed"
        from_account_updated, to_account_updated = self.features.account_transfer_feature.validate_account_balance(user=self.current_user, transfer_percentage=10)
        assert from_account_updated, f"Transfer From balance details not updated."
        assert to_account_updated, f"Transfer to details not updated."

    def teardown_method(self, method):
        super().teardown_method(method)
