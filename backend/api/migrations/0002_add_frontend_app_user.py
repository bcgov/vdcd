from django.db import migrations
from django.conf import settings


def add_frontend_app_user(apps, schema_editor):
    AppUser = apps.get_model("api", "AppUser")
    AppUser.objects.create(app_name=settings.FRONTEND_APP_NAME)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_frontend_app_user),
    ]
