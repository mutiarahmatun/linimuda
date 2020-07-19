from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmetadata.models import MetadataPageMixin


class LayananKamiBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    thumbnail = ImageChooserBlock()


class HomePage(MetadataPageMixin, Page):
    section_layanan_kami = StreamField(
        [("Layanan", LayananKamiBlock())], default="", blank=True
    )
    content_panels = Page.content_panels + [
        InlinePanel("cover_images", label="cover images"),
        StreamFieldPanel("section_layanan_kami"),
    ]


class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="cover_images")
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=150)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
    ]
