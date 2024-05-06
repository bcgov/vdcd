from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_uploadedvinsfile_remove_uploadedvinrecord_model_year_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadedvinrecord',
            options={},
        ),
        migrations.AddField(
            model_name='uploadedvinrecord',
            name='postal_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='uploadedvinrecord',
            name='vin',
            field=models.CharField(max_length=17),
        ),
        migrations.AddConstraint(
            model_name='uploadedvinrecord',
            constraint=models.UniqueConstraint(fields=('vin', 'postal_code'), name='unique_vin_postal_code'),
        ),
    ]
