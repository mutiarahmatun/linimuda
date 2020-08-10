from coderedcms.models import CoderedWebPage
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    InlinePanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.utils.decorators import cached_classmethod


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
    body_content_panels = []
    # section layanan
    section_layanan = StreamField([("Layanan", LayananBlock())], blank=True)
    content_panels = Page.content_panels + [
        InlinePanel("cover_images", label="Cover Images"),
        StreamFieldPanel("section_layanan"),
    ]

    @cached_classmethod
    def get_edit_handler(cls):  # noqa
        """
        Override to "lazy load" the panels overriden by subclasses.
        """
        panels = [
            ObjectList(
                cls.content_panels
                + cls.body_content_panels
                + cls.bottom_content_panels,
                heading=_("Content"),
            ),
            ObjectList(cls.classify_panels, heading=_("Classify")),
            ObjectList(cls.promote_panels, heading=_("SEO"), classname="seo"),
            ObjectList(
                cls.settings_panels, heading=_("Settings"), classname="settings"
            ),
        ]

        if cls.integration_panels:
            panels.append(
                ObjectList(
                    cls.integration_panels,
                    heading="Integrations",
                    classname="integrations",
                )
            )

        return TabbedInterface(panels).bind_to(model=cls)


class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="cover_images")
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    panels = [
        ImageChooserPanel("image"),
    ]
