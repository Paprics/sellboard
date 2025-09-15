import pytest
from django.urls import reverse
from faker import Faker

faker = Faker("uk_UA")
USER_NAME = faker.name()
USER_EMAIL = faker.email()
# USER_PHONE_NUMBER = faker.phone_number()
USER_PHONE_NUMBER = "+380991234567"
USER_PASSWORD = faker.password()


@pytest.mark.django_db
class TestLoginView:

    @pytest.mark.parametrize(
        "login_field,password",
        [
            ("wrong@example.com", "wrongpass"),  # неверный email
            ("+380000000000", "wrongpass"),  # неверный телефон
            ("test@example.com", "wrongpass"),  # правильный логин, неверный пароль
        ],
    )
    def test_login_with_invalid_data(self, client, user_factory, login_field, password):
        # создаём пользователя с правильными данными
        user_factory(
            user_name="Test User", email="test@example.com", phone_number="+380991234567", password="correct_password"
        )

        url = reverse("accounts:login")
        response = client.post(url, {"login": login_field, "password": password})

        # проверяем, что редиректа нет
        assert response.status_code == 200
        # пользователь не аутентифицирован
        assert not response.wsgi_request.user.is_authenticated

    @pytest.mark.parametrize("login_field", [USER_EMAIL, USER_PHONE_NUMBER])
    def test_login_with_user_factory(self, client, user_factory, login_field):
        user = user_factory(
            user_name=USER_NAME, email=USER_EMAIL, phone_number=USER_PHONE_NUMBER, password=USER_PASSWORD
        )
        url = reverse("accounts:login")
        response = client.post(url, {"login": login_field, "password": USER_PASSWORD})
        assert response.status_code == 302
        assert response.wsgi_request.user.is_authenticated


# @pytest.mark.django_db
# def test_login_view(client, django_user_model):
#
#     django_user_model.objects.create_user(username="test", password="123")
#
#     url = reverse("login")
#     response = client.post(url, {"username": "test", "password": "123"})
#     assert response.status_code == 302
