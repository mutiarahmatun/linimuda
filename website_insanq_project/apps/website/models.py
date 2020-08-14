from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import EditHandler, FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import hooks


@hooks.register("construct_settings_menu")
def hide_user_menu_item(request, menu_items):
    hide_item_by_name = [
        "mailchimp-api",
        "accessibility",
        "google-api",
        "mailchimp-api",
        "collections",
        "cache",
    ]
    menu_items[:] = [item for item in menu_items if item.name not in hide_item_by_name]


@register_setting(icon="fa-building-o")
class Profile(BaseSetting):
    """
    Social media accounts.
    """

    class Meta:

        verbose_name = _("Profile")

    company_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("Company Name")
    )
    email = models.EmailField(max_length=255, blank=True, verbose_name=_("Email"))
    telephone_number = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Telephone Number"),
        help_text=_("Don't forget with country code. Example: 62215678901"),
    )
    handphone_number_1 = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Handphone / WhatsApp Number 1"),
        help_text=_("Don't forget with country code. Example: 6281234567890"),
    )
    handphone_number_2 = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Handphone / WhatsApp Number 2"),
        help_text=_("Don't forget with country code. Example: 6281234567890"),
    )
    address = models.CharField(max_length=511, blank=True, verbose_name=_("Address"))

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("company_name"),
                FieldPanel("email"),
                FieldPanel("telephone_number"),
                FieldPanel("handphone_number_1"),
                FieldPanel("handphone_number_2"),
                FieldPanel("address"),
            ],
            _("Profile"),
        )
    ]


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
