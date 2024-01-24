from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('app_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UploadedVinRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('vin', models.CharField(max_length=17, unique=True)),
                ('model_year', models.CharField(max_length=4, null=True)),
                ('vpic_current_decode_successful', models.BooleanField(default=False)),
                ('vpic_number_of_current_decode_attempts', models.IntegerField(default=0)),
                ('vinpower_current_decode_successful', models.BooleanField(default=False)),
                ('vinpower_number_of_current_decode_attempts', models.IntegerField(default=0)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VinpowerDecodedVinRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('vin', models.CharField(max_length=17, unique=True)),
                ('data', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VpicDecodedVinRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('vin', models.CharField(max_length=17, unique=True)),
                ('data', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='api.appuser', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
    ]
