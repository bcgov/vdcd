from django_extensions.db.models import TimeStampedModel
from rest_framework.authtoken.models import Token
from django.db.models import (
    CharField,
    BooleanField,
    OneToOneField,
    IntegerField,
    JSONField,
    CASCADE,
    UniqueConstraint,
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


class UploadedVinsFile(TimeStampedModel):
    filename = CharField(max_length=32, unique=True)

    chunk_size = IntegerField(default=25000)

    chunks_per_run = IntegerField(default=4)

    start_index = IntegerField(default=0)

    processed = BooleanField(default=False)


class UploadedVinRecord(TimeStampedModel):
    vin = CharField(max_length=17)

    postal_code = CharField(max_length=7, null=True, blank=True)

    data = JSONField()

    vpic_current_decode_successful = BooleanField(default=False)

    vpic_number_of_current_decode_attempts = IntegerField(default=0)

    vinpower_current_decode_successful = BooleanField(default=False)

    vinpower_number_of_current_decode_attempts = IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["vin", "postal_code"], name="unique_vin_postal_code"
            )
        ]


class DecodedVinRecord(TimeStampedModel):
    vin = CharField(max_length=17, unique=True)

    data = JSONField()

    class Meta:
        abstract = True


class VpicDecodedVinRecord(DecodedVinRecord):
    pass


class VinpowerDecodedVinRecord(DecodedVinRecord):
    pass
