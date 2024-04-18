from lib.api_service_provider.api_service import APIService
from lib.api_service_provider.api_constants import APIConstants, REFERERConstants
from lib.logger.logger import logger
from lib.data_provider.models.user import User
import re


class UserAPIServiceConstants:
    pass


class UserAPIService(APIService):

    def set_session_cookies(self) -> None:
        self.get(APIConstants.REGISTER)

    def register_user(self, user_data: dict) -> bool:
        """Register user API"""
        self.set_session_cookies()

        # Convert user data to URL-encoded form data
        form_data = '&'.join([f"customer.{key}={value}" for key, value in user_data.items() if key not in ['address', 'repeatedPassword']])
        address_data = '&'.join([f"customer.address.{key}={value}" for key, value in user_data['address'].items()])
        repeated_password = f"&repeatedPassword={user_data['password']}"
        form_data += '&' + address_data + repeated_password

        # Make the POST request
        response = self.post(endpoint=APIConstants.REGISTER, data=form_data, origin=APIConstants.ORIGIN,
                             referer=REFERERConstants.REGISTER)

        confirmation_message = "Your account was created successfully. You are now logged in."

        if confirmation_message not in response.text:
            logger.info("Registration confirmation msg not shown!")
            return False

        first_name = user_data["firstName"]
        last_name = user_data["lastName"]
        name_pattern = rf"<p class=\"smallText\"><b>Welcome<\/b>\s+{re.escape(first_name)}\s+{re.escape(last_name)}<\/p>"
        match = re.search(name_pattern, response.text)
        if match:
            return True
        else:
            print("First name and last name not found. - Name pattern not found")
            return False


    def login_user(self, user: User) -> bool:

        data = {
        'username': user.username,
        'password': user.password}

        response = self.post(endpoint=APIConstants.LOGIN, data=data, allow_redirects=False, origin=APIConstants.ORIGIN, referer=REFERERConstants.LOGIN)
        if response.status_code == 302:
            cookies = response.cookies.get_dict()
            logger.info(f"jsessionid_cookie : {cookies.get('JSESSIONID')}")
            return True
        else:
            logger.info(f"Unable to login")
            return False

    def logout(self) -> bool:
        # Send the request
        response = self.post(endpoint=APIConstants.LOGOUT, allow_redirects=False, referer=REFERERConstants.OVERVIEW)

        # Check if the request was successful
        if response.status_code == APIConstants.STATUS_REDIRECT:
            logger.info("Logout successful")
            new_session_id = response.cookies.get('JSESSIONID')
            logger.info(f"New session id: {new_session_id}")
            return True
        else:
            logger.info("Logout failed:", response.status_code)
            return False

user_api_service = UserAPIService()

