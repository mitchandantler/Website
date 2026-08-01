from django.db import migrations


def create_default_home_page_content(apps, schema_editor):
    HomePageContent = apps.get_model("website", "HomePageContent")
    HomePageContent.objects.get_or_create(pk=1)


def remove_default_home_page_content(apps, schema_editor):
    HomePageContent = apps.get_model("website", "HomePageContent")
    HomePageContent.objects.filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_heroimage_homepagecontent"),
    ]

    operations = [
        migrations.RunPython(
            create_default_home_page_content, remove_default_home_page_content
        ),
    ]
