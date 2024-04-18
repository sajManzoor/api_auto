from random import randint, choices
from string import ascii_letters, digits, ascii_lowercase, ascii_uppercase
from lib.logger.logger import logger


def handle_exceptions(func):
    """ Wrapper function can be used as a decorator - to handle exceptions """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(f"Exception caught in {func.__name__}: {e}")

    return wrapper


def generate_random_phone_number():
    """ Method to generate random phone number """
    return f"{randint(1000000000, 9999999999):010d}"


def generate_random_name_with_prefix(prefix, length=8):
    """ Method to generate random name with prefix and length """
    random_suffix = ''.join(choices(ascii_letters, k=length))
    return f"{prefix}_{random_suffix}"


def generate_random_email(domain="yopmail.com", length=8):
    """ Method to generate random email with domain and length """
    username = ''.join(choices(ascii_lowercase + digits, k=length))
    return f"{username}@{domain}"


def generate_random_ssn():
    """ Method to generate random ssn """
    return '-'.join([''.join(choices(digits, k=3)) for _ in range(3)])


def generate_random_username(length=8):
    """ Method to generate random username with length """
    return ''.join(choices(ascii_letters + digits, k=length))


def generate_random_password(length=8):
    """ Method to generate random password with length """
    return ''.join(choices(ascii_letters + digits, k=length))


def generate_random_address(length=8):
    """ Method to generate random address fields with length """
    street = ''.join(choices(ascii_letters + digits, k=length))
    city = ''.join(choices(ascii_letters, k=length))
    state = ''.join(choices(ascii_uppercase, k=2))
    zip_code = ''.join(choices(digits, k=5))
    return {
        "street": street,
        "city": city,
        "state": state,
        "zipCode": zip_code
    }




