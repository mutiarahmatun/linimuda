# Generated by Django 3.0.8 on 2020-07-13 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0022_uploadedimage"),
        ("home", "0003_auto_20200708_1924"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.Image",
                verbose_name="Search image",
            ),
        ),
    ]
