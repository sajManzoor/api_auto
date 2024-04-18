from lib.data_provider.data_provider import DataProvider
from lib.data_provider.models.user import User
from features.feature_manager import Features
from lib.utils.constants import LIVE


class TestBaseCase:

    def setup_method(self, method) -> None:
        # This method is called before each test method is executed
        self.data_provider = DataProvider(LIVE)
        self.features = Features()
        self.current_user = None

    def teardown_method(self, method) -> None:
        # This method is called after each test method is executed
        # Perform cleanup or resource release here if needed
        self.features.auth_feature.close_session()

    def attempt_login(self, user: User) -> None:
        """Method to attempt Login with static user - if user is not present - register > logout > logout"""
        self.current_user = user
        # attempt login with existing user
        if not self.features.auth_feature.login_user(user=self.current_user):
            self.current_user = User.generate_random()
            assert self.features.auth_feature.register_user(self.current_user.to_dict()), f"Register new user - Failed"
            self.features.auth_feature.logout()
            assert self.features.auth_feature.login_user(self.current_user), f"Login user - Failed"





