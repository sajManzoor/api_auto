from tests.base_case import TestBaseCase
from lib.data_provider.models.user import User


class TestLoginUser(TestBaseCase):

    def setup_method(self, method):
        super().setup_method(method)
        self.normal_user = self.data_provider.get_normal_customer()
        self.new_user = User.generate_random()

    def test_login_user(self):

        # attempt to login exiting user
        if self.features.auth_feature.login_user(self.normal_user):
            assert True
        else:
            assert self.features.auth_feature.register_user(self.new_user.to_dict()), f"Register new user - Failed"
            self.features.auth_feature.logout()
            assert self.features.auth_feature.login_user(self.new_user), f"Login new user - Failed"

    def teardown_method(self, method):
        super().teardown_method(method)
