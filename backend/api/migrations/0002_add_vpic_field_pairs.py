from django.db import migrations


def add_vpic_field_pairs(apps, schema_editor):
    VpicFieldPair = apps.get_model("api", "VpicFieldPair")
    field_name_pairs = [
        {"external": "Make", "internal": "make"},
        {"external": "Model", "internal": "model"},
        {"external": "ModelYear", "internal": "model_year"},
    ]

    for pair in field_name_pairs:
        VpicFieldPair.objects.create(
            external_field_name=pair["external"], internal_field_name=pair["internal"]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_vpic_field_pairs),
    ]
