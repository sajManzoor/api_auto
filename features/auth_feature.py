from lib.api_service_provider.user.user_api_service import user_api_service
from lib.data_provider.models.user import User


class AuthFeature:

    def register_user(self, data):
        return user_api_service.register_user(data)

    def login_user(self, user: User):
        return user_api_service.login_user(user)

    def logout(self):
        return user_api_service.logout()

    def close_session(self):
        user_api_service.close_session()
