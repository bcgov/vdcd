from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_add_frontend_app_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedVinsFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('filename', models.CharField(max_length=32, unique=True)),
                ('chunk_size', models.IntegerField(default=25000)),
                ('chunks_per_run', models.IntegerField(default=4)),
                ('start_index', models.IntegerField(default=0)),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='uploadedvinrecord',
            name='model_year',
        ),
        migrations.AddField(
            model_name='uploadedvinrecord',
            name='data',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
