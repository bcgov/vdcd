from django.core.management.base import BaseCommand, CommandError
from api.models import AppUser, AppToken
from django.conf import settings
from django.db import transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        app_name = options["app_name"]

        if app_name == settings.FRONTEND_APP_NAME:
            raise CommandError(
                "{} service should not have a token associated with it".format(app_name)
            )
        try:
            app_user = AppUser.objects.create(app_name=app_name)
            token = AppToken.objects.create(user=app_user)
        except Exception:
            raise CommandError("Error generating user and token")

        self.stdout.write("Generated token {} for app {}".format(token.key, app_name))
