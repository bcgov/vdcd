from django_extensions.db.models import TimeStampedModel
from rest_framework.authtoken.models import Token
from django.db.models import (
    CharField,
    BooleanField,
    OneToOneField,
    IntegerField,
    JSONField,
    CASCADE,
)
from django.utils.translation import gettext_lazy as _


class AppUser(TimeStampedModel):
    is_active = BooleanField(default=True)

    app_name = CharField(max_length=100, unique=True)

    @property
    def is_authenticated(self):
        return True


class AppToken(Token):
    user = OneToOneField(
        AppUser,
        related_name="auth_token",
        on_delete=CASCADE,
        verbose_name=_("User"),
    )


class UploadedVinRecord(TimeStampedModel):
    vin = CharField(max_length=17, unique=True)

    model_year = CharField(max_length=4, null=True)

    vpic_current_decode_successful = BooleanField(default=False)

    vpic_number_of_current_decode_attempts = IntegerField(default=0)

    vinpower_current_decode_successful = BooleanField(default=False)

    vinpower_number_of_current_decode_attempts = IntegerField(default=0)


class DecodedVinRecord(TimeStampedModel):
    vin = CharField(max_length=17, unique=True)

    data = JSONField()

    class Meta:
        abstract = True


class VpicDecodedVinRecord(DecodedVinRecord):
    pass


class VinpowerDecodedVinRecord(DecodedVinRecord):
    pass
