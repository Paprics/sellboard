from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

UserModel = get_user_model()


class EmailOrPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        user = None

        try:
            validate_email(username)
            user = UserModel.objects.filter(email__iexact=username).first()
        except ValidationError:
            user = UserModel.objects.filter(phone_number=username).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
