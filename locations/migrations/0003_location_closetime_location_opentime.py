# Generated by Django 4.2.5 on 2023-11-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0002_location_approved"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="CLOSETIME",
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name="location",
            name="OPENTIME",
            field=models.CharField(default=None, max_length=200),
        ),
    ]
