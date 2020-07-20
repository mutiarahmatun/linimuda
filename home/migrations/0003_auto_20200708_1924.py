# Generated by Django 3.0.8 on 2020-07-08 12:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0022_uploadedimage"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="section_layanan_kami",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "Layanan",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("title", wagtail.core.blocks.CharBlock()),
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
        migrations.CreateModel(
            name="HomePageGalleryImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("caption", models.CharField(blank=True, max_length=150)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cover_images",
                        to="home.HomePage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]
