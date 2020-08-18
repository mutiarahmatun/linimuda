# Generated by Django 3.0.9 on 2020-08-18 04:15

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200818_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='friday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='long_description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='monday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='saturday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='short_description',
            field=wagtail.core.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='sunday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='thursday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='tuesday',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='wednesday',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
