from lib.utils.constants import TIME_SECS_MED
import requests

SESSION = None


def session():
    global SESSION
    SESSION = requests.session()
    SESSION.TIMEOUT = TIME_SECS_MED
    return SESSION


def pytest_configure(config):
    session()
