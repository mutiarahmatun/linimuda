from coderedcms.models import CoderedWebPage
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class LayananBlock(blocks.StructBlock):

    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    thumbnail = ImageChooserBlock()


class HomePage(CoderedWebPage):
    class Meta:
        verbose_name = "Home"

    ###############
    # Panels
    ###############
    layout_panels = []
    settings_panels = Page.settings_panels

    # section layanan
    section_layanan = StreamField([("Layanan", LayananBlock())], blank=True)
    content_panels = Page.content_panels + [
        InlinePanel("cover_images", label="Cover Images"),
        StreamFieldPanel("section_layanan"),
    ]


class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="cover_images")
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    panels = [
        ImageChooserPanel("image"),
    ]
