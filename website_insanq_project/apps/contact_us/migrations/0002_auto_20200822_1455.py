# Generated by Django 3.0.9 on 2020-08-22 07:55

from django.db import migrations, models
import website_insanq_project.apps.contact_us.models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactuspage',
            name='to_address',
            field=models.CharField(blank=True, default=website_insanq_project.apps.contact_us.models.get_email, help_text='Optional - email form submissions to this address. Separate multiple addresses by comma.', max_length=255, verbose_name='Email form submissions to'),
        ),
    ]
