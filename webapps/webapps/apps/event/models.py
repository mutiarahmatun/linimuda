import locale
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.models import Page, Site
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList,
    FieldRowPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from webapps.apps.website.models import ReadOnlyPanel
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedEmail,
    CoderedWebPage,
    CoderedFormPage,
)
from datetime import date, time
from webapps.apps.website.wagtail_hooks import Profile


def get_email():
    return getattr(
        Profile.for_site(Site.objects.get(is_default_site=True)), "email", None
    )


class EventPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Event Page"

    hits = models.IntegerField(default=0, editable=False)

    short_description = RichTextField()
    long_description = RichTextField(blank=True, null=True)

    start_date = models.DateField(null=True, blank=True, default=date.today)
    end_date = models.DateField(null=True, blank=True, default=date.today)
    start_time_each_day = models.TimeField(null=True, blank=True, default=time(8, 0, 0))
    end_time_each_day = models.TimeField(null=True, blank=True, default=time(16, 0, 0))
    location = models.CharField(blank=True, max_length=1023, default="LiniMuda", null=True)
    [monday, tuesday, wednesday, thursday, friday, saturday, sunday,] = [
        models.BooleanField(default=True) for _ in range(7)
    ]

    to_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=get_email,
        verbose_name=_("Email form submissions to"),
        help_text=_(
            "Optional - email form submissions to this address. Separate multiple addresses by comma."
        ),  # noqa
    )

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    def format(self, attr_name, format):
        locale.setlocale(locale.LC_ALL, "en_US")
        attr_value = getattr(self, attr_name, None)
        return attr_value.strftime(format) if attr_value else ""

    def get_start_date(self):
        return self.format("start_date", "%d %B %Y")

    def get_end_date(self):
        return self.format("end_date", "%d %B %Y")

    def get_start_time_each_day(self):
        return self.format("start_time_each_day", "%H.%M")

    def get_end_time_each_day(self):
        return self.format("end_time_each_day", "%H.%M")

    template = "event/event_page.html"
    landing_page_template = "thank_you_page.html"

    # Friend panels
    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
                ImageChooserPanel("og_image"),
            ],
            _("Page Meta Data"),
        ),
    ]

    body_content_panels = (
        [
            InlinePanel(
                "form_fields",
                label="Form fields registration event",
                help_text="Don't forget to specify date and time registrant choice's",
            )
        ]
        + [
            MultiFieldPanel(
                [
                    FieldPanel("start_date"),
                    FieldPanel("end_date"),
                    FieldPanel("start_time_each_day"),
                    FieldPanel("end_time_each_day"),
                    FieldPanel("location"),
                ],
                _("Event Details"),
            )
        ]
        + [
            MultiFieldPanel(
                [
                    FieldPanel("monday"),
                    FieldPanel("tuesday"),
                    FieldPanel("wednesday"),
                    FieldPanel("thursday"),
                    FieldPanel("friday"),
                    FieldPanel("saturday"),
                    FieldPanel("sunday"),
                ],
                _("Event Days"),
            ),
        ]
        + [
            MultiFieldPanel(
                [
                    FieldPanel("short_description", classname="full"),
                    FieldPanel("long_description", classname="full"),
                ],
                _("Event Description"),
            )
        ]
        + [
            MultiFieldPanel(
                [
                    FieldPanel("save_to_database"),
                    FieldPanel("to_address"),
                    FieldPanel("reply_address"),
                    FieldPanel("subject"),
                ],
                _("Form Submissions"),
            ),
        ]
        + [
            MultiFieldPanel(
                [ReadOnlyPanel("hits", heading="Hits")], _("Publication Info")
            )
        ]
    )
    content_panels = Page.content_panels
    layout_panels = []

    integration_panels = []

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("form_golive_at"), FieldPanel("form_expire_at"),],
                    classname="label-above",
                ),
            ],
            _("Form Scheduled Publishing"),
        ),
        FieldPanel("spam_protection"),
    ]

    # Override edit_handler to not contain layout tabs
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

    search_fields = CoderedFormPage.search_fields + [
        index.SearchField("short_description", partial_match=True),
        index.SearchField("long_description", partial_match=True),
    ]

    # Only allow this page to be created beneath an EventIndexPage.
    parent_page_types = ["event.EventIndexPage"]


class EventPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("EventPage", related_name="form_fields")


class EventConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("EventPage", related_name="confirmation_emails")


class EventIndexPage(CoderedWebPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Event Landing Page"

    hits = models.IntegerField(default=0, editable=False)
    body = None

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    search_fields = []
    # Panel
    # Friend panels
    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
                ImageChooserPanel("og_image"),
            ],
            _("Page Meta Data"),
        ),
    ]

    # Override to not contain template form
    layout_panels = []

    # Override to become empty
    body_content_panels = []

    # Override without content walls
    settings_panels = Page.settings_panels

    # Override with additional hits attribute
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [ReadOnlyPanel("hits", heading="Hits"),], _("Publication Info"),
        ),
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

    template = "event/event_index_page.html"

    index_show_subpages_default = True
    index_order_by_default = "title"
    index_query_pagemodel = "event.EventPage"

    # Only allow EventPages beneath this page.
    parent_page_types = ["home.HomePage"]
