from django.db import migrations

CATEGORIES = [
    ("All Day Menu", "food", 0),
    ("Little Ones", "food", 1),
    ("Coffee and Frappes", "drink", 2),
    ("Cold Beverages", "drink", 3),
    ("Cold Drinks", "drink", 4),
]


def create_categories(apps, schema_editor):
    MenuCategory = apps.get_model("menu", "MenuCategory")
    for name, menu_type, display_order in CATEGORIES:
        MenuCategory.objects.get_or_create(
            name=name,
            defaults={"menu_type": menu_type, "display_order": display_order},
        )


def remove_categories(apps, schema_editor):
    MenuCategory = apps.get_model("menu", "MenuCategory")
    MenuCategory.objects.filter(name__in=[name for name, _, _ in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]
