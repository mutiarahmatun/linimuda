from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from coderedcms.models.snippet_models import Classifier
from .models import Navbar


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


@hooks.register("construct_main_menu")
def hide_main_menu(request, menu_items):
    hide_menu_by_name = ["snippets"]
    print([item.name for item in menu_items])
    menu_items[:] = [item for item in menu_items if item.name not in hide_menu_by_name]


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


class NavbarAdmin(ModelAdmin):
    model = Navbar
    menu_label = "Navbar"
    menu_icon = "list-ul"
    menu_order = 499
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)


class ClassifierAdmin(ModelAdmin):
    model = Classifier
    menu_label = "Classifier"
    menu_icon = "folder-inverse"
    menu_order = 500
    add_to_settingsmenu = False
    exclude_from_explorer = False
    list_display = ("name",)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(NavbarAdmin)
modeladmin_register(ClassifierAdmin)
