# Generated by Django 3.0.8 on 2020-07-19 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="articlepage", name="coba",),
    ]
