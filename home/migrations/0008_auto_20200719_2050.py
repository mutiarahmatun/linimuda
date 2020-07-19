# Generated by Django 3.0.8 on 2020-07-19 13:50

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_auto_20200719_2039"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="section_layanan_kami",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "Layanan",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("titleeee", wagtail.core.blocks.CharBlock()),
                                ("content", wagtail.core.blocks.RichTextBlock()),
                                (
                                    "thumbnail",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                default="",
            ),
        ),
    ]
