import locale
from django.utils import timezone
from coderedcms.models import CoderedArticleIndexPage, CoderedArticlePage
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
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from website_insanq_project.apps.website.models import ReadOnlyPanel


class VideoPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Video Page"
        ordering = [
            "-first_published_at",
        ]

    # Override to have default today
    date_display = models.DateTimeField(
        verbose_name=_("Publish date"), default=timezone.now
    )

    link_thumbnail_embed_video = models.URLField(max_length=511)

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
        locale.setlocale(locale.LC_ALL, "id_ID")
        if hasattr(self, "date_display") and self.date_display:
            return self.date_display.strftime("%d %B %Y")
        return ""

    template = "video/video_page.html"

    # Override to become empty
    layout_panels = []

    # Override to become empty
    body_content_panels = []

    # Override without content walls
    settings_panels = Page.settings_panels

    # Override with additional hits attribute
    content_panels = (
        Page.content_panels
        + [FieldPanel("link_thumbnail_embed_video")]
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

    search_fields = CoderedArticlePage.search_fields + [
        index.SearchField("body_text", partial_match=True)
    ]

    parent_page_types = ["video.VideoIndexPage"]


class VideoIndexPage(CoderedArticleIndexPage):
    class Meta:
        verbose_name = "Video Landing Page"

    hits = models.IntegerField(default=0, editable=False)
    body = None

    def add_hits(self):
        self.hits += 1
        self._meta.get_field("index_order_by").choices = self.index_order_by_choices
        self.save()
        return ""

    search_fields = []
    # Panel

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

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "video.VideoPage"

    template = "video/video_index_page.html"

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

    # Only allow VideoPages beneath this page.
    parent_page_types = ["home.HomePage"]
