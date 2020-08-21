from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedEmail, CoderedFormPage
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.core.models import Page
from wagtail.utils.decorators import cached_classmethod


from website_insanq_project.apps.website.models import ReadOnlyPanel


class ContactUsPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Contact Us Page"

    hits = models.IntegerField(default=0, editable=False)
    html_embedded_maps = models.CharField(max_length=511, blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image", null=True, on_delete=models.SET_NULL, related_name="+",
    )

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    search_fields = [
        index.FilterField("title"),
    ]

    template = "contact_us/contact_us_page.html"
    landing_page_template = "thank_you_page.html"

    content_panels = Page.content_panels + [
        ImageChooserPanel("main_image"),
    ]

    body_content_panels = (
        [FieldPanel("html_embedded_maps")]
        + [InlinePanel("form_fields", label="Form fields"),]
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
            FormSubmissionsPanel(),
        ]
        + [
            MultiFieldPanel(
                [ReadOnlyPanel("hits", heading="Hits")], _("Publication Info")
            )
        ]
    )

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

    parent_page_types = ["home.HomePage"]


class ContactUsPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("ContactUsPage", related_name="form_fields")


class ContactUsConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("ContactUsPage", related_name="confirmation_emails")
