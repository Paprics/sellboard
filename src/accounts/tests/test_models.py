import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from faker import Faker

from accounts.models import Profile

faker = Faker("uk_UA")
USER_NAME = faker.name()
USER_EMAIL = faker.email()
# USER_PHONE_NUMBER = faker.phone_number()
USER_PHONE_NUMBER = "+380991234567"
USER_PASSWORD = faker.password()

USER = get_user_model()


@pytest.mark.django_db
def test_profile_created_on_user_creation():
    user = USER.objects.create_user(
        user_name=USER_NAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
        phone_number=USER_PHONE_NUMBER,
    )
    profile = Profile.objects.get(user=user)
    assert profile.user == user
    assert user.check_password(USER_PASSWORD)
    assert Profile.objects.filter(user=user).count() == 1


@pytest.mark.django_db
class TestUserRegistrationModel:

    @pytest.mark.parametrize(
        "user_name, email, phone_number, password",
        [
            # (None, USER_EMAIL, USER_PHONE_NUMBER, USER_PASSWORD),
            (USER_NAME, None, USER_PHONE_NUMBER, USER_PASSWORD),
            (USER_NAME, USER_EMAIL, None, USER_PASSWORD),
            (USER_NAME, USER_EMAIL, USER_PHONE_NUMBER, None),
        ],
    )
    def test_user_fields_must_be_present_manager(self, user_name, email, phone_number, password):
        "Manager test: Test for missing required registration field"
        with pytest.raises((ValueError, ValidationError)):
            user_obj = USER.objects.create_user(
                user_name=user_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )

    # ----------------------------------------------

    @pytest.mark.parametrize(
        "user_name, email, phone_number",
        [(None, USER_EMAIL, USER_PHONE_NUMBER), (USER_NAME, None, USER_PHONE_NUMBER), (USER_NAME, USER_EMAIL, None)],
    )
    def test_user_fields_must_be_present_model(self, user_name, email, phone_number):
        "Model test: Test for missing required registration field"
        with pytest.raises(ValidationError):
            user_obj = USER.objects.create(
                user_name=USER_NAME,
                email=USER_EMAIL,
                phone_number=USER_PHONE_NUMBER,
            )
            user_obj.full_clean()
