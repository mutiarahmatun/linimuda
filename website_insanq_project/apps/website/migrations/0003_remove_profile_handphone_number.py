# Generated by Django 3.0.7 on 2020-08-11 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_profile_telephone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='handphone_number',
        ),
    ]
