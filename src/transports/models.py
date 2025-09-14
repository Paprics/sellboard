import shortuuid
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

user_model = get_user_model()


def generate_uuid():
    return shortuuid.uuid()


class Transport(models.Model):

    owner = models.OneToOneField(user_model, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=22, unique=True, default=generate_uuid, editable=False, db_index=True)
    license_plate = models.CharField(max_length=15)
    vin_code = models.CharField(max_length=25)
    date_created = models.DateTimeField(auto_now_add=True)

    condition = models.CharField()
    type_avto = models.CharField()
    body_type = models.CharField()
    car_model = models.CharField()
    year_issue = models.CharField()
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField()
    color = models.CharField()
    engine_cc = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)], verbose_name="Engine volume in liters"
    )
    type_fuel = models.CharField()
    type_transmission = models.CharField()
    drive_type = models.CharField()

    class Meta:
        verbose_name = "transport"
        verbose_name_plural = "transports"
        db_table = "transport"
        abstract = True

    def __str__(self):
        return f"{self.owner.username} transport"
