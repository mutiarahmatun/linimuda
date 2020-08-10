from datetime import date

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
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from website_insanq_project.apps.website.models import ReadOnlyPanel


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = [
            "-first_published_at",
        ]

    # Override to have default today
    date_display = models.DateField(
        null=True, blank=True, verbose_name=_("Publish date"), default=date.today
    )

    # Additional attribute
    hits = models.IntegerField(default=0, editable=False)

    # Override from streamfield to richtextfield
    body_text = RichTextField(blank=False, verbose_name=_("body"))

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

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    # Override to become empty
    layout_panels = []

    # Override to become empty
    body_content_panels = []

    # Override without content walls
    settings_panels = Page.settings_panels

    # Override with additional hits attribute
    content_panels = (
        Page.content_panels
        + [ImageChooserPanel("cover_image"),]
        + [
            MultiFieldPanel(
                [
                    FieldPanel("author"),
                    FieldPanel("author_display"),
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
        index.SearchField("body", partial_match=True)
    ]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["article.ArticleIndexPage"]
    subpage_types = []


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    hits = models.IntegerField(default=0, editable=False)
    body = None

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

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
    index_query_pagemodel = "article.ArticlePage"

    template = "coderedcms/pages/article_index_page.html"

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

    # Only allow ArticlePages beneath this page.
    subpage_types = ["article.ArticlePage"]
