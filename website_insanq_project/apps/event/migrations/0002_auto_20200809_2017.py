# Generated by Django 3.0.7 on 2020-08-09 13:17

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventpage',
            options={'verbose_name': 'Event Page'},
        ),
        migrations.AddField(
            model_name='eventpage',
            name='long_description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
