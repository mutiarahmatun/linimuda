from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Navbar
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.translation import gettext_lazy as _
from coderedcms.models.snippet_models import Classifier
from wagtail.admin.edit_handlers import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)

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
    copyright_year = models.IntegerField(
        null=True, blank=True, verbose_name=_("Copyright Year")
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
                FieldPanel("copyright_year"),
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