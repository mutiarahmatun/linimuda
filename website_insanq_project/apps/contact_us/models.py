from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    FieldRowPanel,
)
from website_insanq_project.apps.website.models import ReadOnlyPanel
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedEmail,
    CoderedFormPage,
)


class ContactUsPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Contact Us Page"

    hits = models.IntegerField(default=0, editable=False)
    url_embedded_maps = models.URLField(max_length=511, blank=True)

    def add_hits(self):
        self.hits += 1
        self.save()

    template = "coderedcms/pages/form_page.html"

    body_content_panels = (
        [FieldPanel("url_embedded_maps")]
        + [InlinePanel("form_fields", label="Form fields"),]
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
