from tests.base_case import TestBaseCase
from lib.data_provider.models.user import User


class TestRegisterUser(TestBaseCase):

    def setup_method(self, method):
        super().setup_method(method)
        self.new_user = User.generate_random()

    def test_register_user(self):
        assert self.features.auth_feature.register_user(self.new_user.to_dict()), f"Assertion Failed, Unable to register new user"

    def teardown_method(self, method):
        super().teardown_method(method)
