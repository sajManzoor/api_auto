from lib.utils.helper import generate_random_password, generate_random_name_with_prefix, generate_random_address, generate_random_ssn, generate_random_phone_number, generate_random_username
from enum import Enum


class User:
    def __init__(self, data):
        self.data = data["customer"]
        self.firstName = self.data['firstName']
        self.lastName = self.data['lastName']
        self.street = self.data['address']['street']
        self.city = self.data['address']['city']
        self.state = self.data['address']['state']
        self.zipCode = self.data['address']['zipCode']
        self.phoneNumber = self.data['phoneNumber']
        self.ssn = self.data['ssn']
        self.username = self.data['username']
        self.password = self.data['password']
        self.customerId = 0
        self.accounts = []

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_dict(self):
        return self.data

    @classmethod
    def generate_random(cls):
        password = generate_random_password()
        data = {
            'customer': {
                'firstName': generate_random_name_with_prefix("TestFirst"),
                'lastName': generate_random_name_with_prefix("TestLast"),
                'address': generate_random_address(),
                'phoneNumber': generate_random_phone_number(),
                'ssn': generate_random_ssn(),
                'username': generate_random_username(),
                'password': password,
                'repeatedPassword': password
            }
        }
        return cls(data)


class AccountType(Enum):
    Checking = 0
    Savings = 1


class Account:
    def __init__(self, data):
        self.id = data['id']
        self.customerId = data['customerId']
        self.type = data['type']
        self.balance = data['balance']
