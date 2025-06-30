import pytest


@pytest.fixture
def numbers():
    return "1234 56** **** 5678"


@pytest.fixture
def numbers_unusual():
    return "1234 56** **** 5678"


@pytest.fixture
def numbers_short():
    return "1234 56** **** 7890"


@pytest.fixture
def numbers_account():
    return "**7890"


@pytest.fixture
def numbers_account_short():
    return "**1234"
