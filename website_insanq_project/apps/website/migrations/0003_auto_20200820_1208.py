# Generated by Django 3.0.9 on 2020-08-20 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_profile_copyright_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='copyright_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Copyright Year'),
        ),
    ]
