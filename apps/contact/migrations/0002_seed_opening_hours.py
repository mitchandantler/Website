from django.db import migrations


def create_default_opening_hours(apps, schema_editor):
    OpeningHours = apps.get_model("contact", "OpeningHours")
    for day_of_week in range(7):
        OpeningHours.objects.get_or_create(
            day_of_week=day_of_week, defaults={"is_closed": True}
        )


def remove_default_opening_hours(apps, schema_editor):
    OpeningHours = apps.get_model("contact", "OpeningHours")
    OpeningHours.objects.filter(day_of_week__in=range(7)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_default_opening_hours, remove_default_opening_hours
        ),
    ]
