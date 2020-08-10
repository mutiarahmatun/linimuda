from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    FieldRowPanel,
)
from wagtail.search import index
from website_insanq_project.apps.website.models import ReadOnlyPanel
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedEmail,
    CoderedFormPage,
)
from datetime import date, time


class EventPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Event Page"

    hits = models.IntegerField(default=0, editable=False)

    short_description = RichTextField(blank=True)
    long_description = RichTextField(blank=True)

    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    start_time_each_day = models.TimeField(default=time(8, 0, 0))
    end_time_each_day = models.TimeField(default=time(16, 0, 0))
    location = models.CharField(max_length=511, default="Insan-Q Cilegon")
    [monday, tuesday, wednesday, thursday, friday, saturday, sunday,] = [
        models.BooleanField(default=True) for _ in range(7)
    ]

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    template = "coderedcms/pages/form_page.html"

    body_content_panels = (
        [InlinePanel("form_fields", label="Form fields"),]
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
                    PageChooserPanel("thank_you_page"),
                    FieldPanel("save_to_database"),
                    FieldPanel("to_address"),
                    FieldPanel("reply_address"),
                    FieldPanel("subject"),
                ],
                _("Form Submissions"),
            ),
        ]
        + [
            FormSubmissionsPanel(),
            InlinePanel("confirmation_emails", label=_("Confirmation Emails")),
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
