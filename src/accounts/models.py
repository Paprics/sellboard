# from django.contrib.auth.models.User
import shortuuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager


def generate_uuid():
    return shortuuid.uuid()


class CustomUser(AbstractBaseUser, PermissionsMixin):

    uuid = models.CharField(max_length=22, unique=True, default=generate_uuid, editable=False, db_index=True)

    phone_number = PhoneNumberField(unique=True)

    email = models.EmailField(
        _("email address"),
        validators=[
            EmailValidator(),
        ],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        unique=True,
    )

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def __str__(self):
        return f"{self.phone_number} {self.first_name}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    info = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        db_table = "user_profile"
