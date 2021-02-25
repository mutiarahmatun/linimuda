"""
Creatable pages used in CodeRed CMS.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from wagtail.admin.edit_handlers import (
    FieldPanel,
    EditHandler,
    StreamFieldPanel,
)

from wagtail.core import blocks
from wagtail.core.fields import StreamField

class ReadOnlyPanel(EditHandler):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )

    def render(self):
        value = getattr(self.instance, self.attr)
        if callable(value):
            value = value()
        return format_html(
            '<div style="padding-top: 0.3em; font-size: 16px;">{}</div>', value,
        )

    def render_as_object(self):
        return format_html(
            "<fieldset><legend>{}</legend>"
            '<ul class="fields"><li><div class="field">{}</div></li></ul>'
            "</fieldset>",
            self.heading,
            self.render(),
        )

    def render_as_field(self):
        return format_html(
            '<div class="field">'
            "<label>{}{}</label>"
            '<div class="field-content">{}</div>'
            "</div>",
            self.heading,
            ":",
            self.render(),
        )

class PageLinkBlock(blocks.StructBlock):
    """
    A component of information with image, text, and buttons.
    """

    display_text = blocks.CharBlock(max_length=255)
    page = blocks.PageChooserBlock(required=False)
    external_url = blocks.URLBlock(
        required=False, help_text="External URL will be prioritized over page link"
    )

class BlockPageLinkBlock(blocks.StructBlock):
    display_text = blocks.CharBlock(max_length=255)
    sub_links = blocks.StreamBlock([("SubLink", PageLinkBlock())])

class Navbar(models.Model):
    class Meta:
        verbose_name = _("Navigation Bar")

    name = models.CharField(max_length=255)
    navigation_links = StreamField(
        [("NonDropdown", PageLinkBlock()), ("Dropdown", BlockPageLinkBlock())],
        blank=True,
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("navigation_links"),
    ]

    def __str__(self):
        return self.name