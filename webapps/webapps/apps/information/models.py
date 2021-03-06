import locale
from django.utils import timezone
from coderedcms.models import CoderedArticlePage
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.utils.decorators import cached_classmethod
from wagtail.images.edit_handlers import ImageChooserPanel
from webapps.apps.website.models import ReadOnlyPanel


class InformationPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Information Page"
        ordering = [
            "-first_published_at",
        ]

    # Override to have default today
    date_display = models.DateTimeField(
        verbose_name=_("Publish date"), default=timezone.now
    )

    # Additional attribute
    hits = models.IntegerField(default=0, editable=False)

    # Override from streamfield to richtextfield
    body_text = RichTextField(verbose_name=_("body"))

    @property
    def body(self):
        return self.body_text

    @body.setter
    def body(self, body):
        self.body_text = body

    # get set
    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    def get_pub_date(self):
        """
        Gets published date.
        """
        locale.setlocale(locale.LC_ALL, "en_US")
        if hasattr(self, "date_display") and self.date_display:
            return self.date_display.strftime("%d %B %Y")
        return ""

    template = "information/information_page.html"

    search_fields = []

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

    # Override to become empty
    layout_panels = []

    # Override to become empty
    body_content_panels = []

    # Override without content walls
    settings_panels = Page.settings_panels

    # Override with additional hits attribute
    content_panels = (
        Page.content_panels
        + [
            MultiFieldPanel(
                [
                    FieldPanel("author"),
                    FieldPanel("date_display"),
                    ReadOnlyPanel("hits", heading="Hits"),
                ],
                _("Publication Info"),
            ),
        ]
        + [FieldPanel("body_text", classname="full",),]
    )

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

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["home.HomePage"]
