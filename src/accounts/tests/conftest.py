# conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_factory(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def default_test_user(db):
    return User.objects.create_user(
        username="test_user",
        email="taet@example.com",
        phone_number="+380991234567",
        password="staticpassword123",
    )
