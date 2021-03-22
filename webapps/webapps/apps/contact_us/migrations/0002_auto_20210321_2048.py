# Generated by Django 3.0.13 on 2021-03-21 13:48

from django.db import migrations, models
import webapps.apps.contact_us.models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactuspage',
            name='html_embedded_maps',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='to_address',
            field=models.CharField(blank=True, default=webapps.apps.contact_us.models.get_email, help_text='Optional - email form submissions to this address. Separate multiple addresses by comma.', max_length=255, null=True, verbose_name='Email form submissions to'),
        ),
    ]
