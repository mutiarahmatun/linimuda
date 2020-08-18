# Generated by Django 3.0.9 on 2020-08-18 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopage',
            name='date_display',
            field=models.DateField(default=datetime.date.today, verbose_name='Publish date'),
        ),
        migrations.AlterField(
            model_name='videopage',
            name='link_thumbnail_embed_video',
            field=models.URLField(max_length=511),
        ),
    ]
