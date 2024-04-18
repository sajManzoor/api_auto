import json
from .models.user import User
import os


class DataProvider:
    _instance = None

    def __new__(cls, env):
        if not cls._instance:
            cls._instance = super(DataProvider, cls).__new__(cls)
            cls._instance.env = env
        return cls._instance

    def get_user_data(self):
        # Get the directory of the current script
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        file_path = f"{current_directory}/{self.env}/user_data.json"
        with open(file_path, 'r') as file:
            user_data = json.load(file)
        return user_data

    def get_normal_customer(self):
        # Get data for normal customer
        user_data = self.get_user_data()
        normal_user_data = user_data["normal_user"]
        return User.from_json(normal_user_data)
