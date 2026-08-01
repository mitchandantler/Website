from django.db import migrations


def create_default_site_setting(apps, schema_editor):
    SiteSetting = apps.get_model("common", "SiteSetting")
    SiteSetting.objects.get_or_create(pk=1)


def remove_default_site_setting(apps, schema_editor):
    SiteSetting = apps.get_model("common", "SiteSetting")
    SiteSetting.objects.filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_site_setting, remove_default_site_setting),
    ]
