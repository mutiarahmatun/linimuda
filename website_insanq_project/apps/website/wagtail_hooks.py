from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from coderedcms.models.snippet_models import Classifier
from .models import Navbar
from coderedcms import schema
from wagtail.images import get_image_model_string
from coderedcms.blocks import (
    OpenHoursBlock,
    StructuredDataActionBlock,
)
from wagtail.core.fields import StreamField


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
    menu_items[:] = [item for item in menu_items if item.name not in hide_menu_by_name]


@register_setting(icon="fa-star-o")
class SeoDefault(BaseSetting):
    """
    Social media accounts.
    """

    class Meta:
        verbose_name = _("SEO Default Each Page")

    ###############
    # SEO fields
    ###############

    search_description = models.CharField(blank=True, max_length=1023,)

    struct_org_type = models.CharField(
        default="",
        blank=True,
        max_length=255,
        choices=schema.SCHEMA_ORG_CHOICES,
        verbose_name=_("Organization type"),
        help_text=_("If blank, no structured data will be used on this page."),
    )
    struct_org_name = models.CharField(
        default="",
        blank=True,
        max_length=255,
        verbose_name=_("Organization name"),
        help_text=_("Leave blank to use the site name in Settings > Sites"),
    )
    struct_org_logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Organization logo"),
        help_text=_("Leave blank to use the logo in Settings > Layout > Logo"),
    )
    struct_org_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Photo of Organization"),
        help_text=_(
            "A photo of the facility. This photo will be cropped to 1:1, 4:3, and 16:9 aspect ratios automatically."
        ),  # noqa
    )
    struct_org_phone = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Telephone number"),
        help_text=_(
            "Include country code for best results. For example: +1-216-555-8000"
        ),
    )
    struct_org_address_street = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Street address"),
        help_text=_(
            "House number and street. For example, 55 Public Square Suite 1710"
        ),
    )
    struct_org_address_locality = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("City"),
        help_text=_("City or locality. For example, Cleveland"),
    )
    struct_org_address_region = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("State"),
        help_text=_("State, province, county, or region. For example, OH"),
    )
    struct_org_address_postal = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Postal code"),
        help_text=_("Zip or postal code. For example, 44113"),
    )
    struct_org_address_country = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Country"),
        help_text=_(
            "For example, USA. Two-letter ISO 3166-1 alpha-2 country code is also acceptible https://en.wikipedia.org/wiki/ISO_3166-1"
        ),  # noqa
    )
    struct_org_geo_lat = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=8,
        verbose_name=_("Geographic latitude"),
    )
    struct_org_geo_lng = models.DecimalField(
        blank=True,
        null=True,
        max_digits=11,
        decimal_places=8,
        verbose_name=_("Geographic longitude"),
    )
    struct_org_hours = StreamField(
        [("hours", OpenHoursBlock()),], blank=True, verbose_name=_("Hours of operation")
    )
    struct_org_actions = StreamField(
        [("actions", StructuredDataActionBlock())],
        blank=True,
        verbose_name=_("Actions"),
    )
    struct_org_extra_json = models.TextField(
        blank=True,
        verbose_name=_("Additional Organization markup"),
        help_text=_(
            "Additional JSON-LD inserted into the Organization dictionary. Must be properties of https://schema.org/Organization or the selected organization type."
        ),  # noqa
    )

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

    panels = [
        MultiFieldPanel([FieldPanel("search_description"),], _("Page Meta Data"),),
        MultiFieldPanel(
            [
                HelpPanel(
                    heading=_("About Organization Structured Data"),
                    content=_(
                        """The fields below help define brand, contact, and storefront
                    information to search engines. This information should be filled out on
                    the site’s root page (Home Page). If your organization has multiple locations,
                    then also fill this info out on each location page using that particular
                    location’s info."""
                    ),
                ),
                FieldPanel("struct_org_type"),
                FieldPanel("struct_org_name"),
                ImageChooserPanel("struct_org_logo"),
                ImageChooserPanel("struct_org_image"),
                FieldPanel("struct_org_phone"),
                FieldPanel("struct_org_address_street"),
                FieldPanel("struct_org_address_locality"),
                FieldPanel("struct_org_address_region"),
                FieldPanel("struct_org_address_postal"),
                FieldPanel("struct_org_address_country"),
                FieldPanel("struct_org_geo_lat"),
                FieldPanel("struct_org_geo_lng"),
                StreamFieldPanel("struct_org_hours"),
                StreamFieldPanel("struct_org_actions"),
                FieldPanel("struct_org_extra_json"),
            ],
            _("Structured Data - Organization"),
        ),
    ]


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
