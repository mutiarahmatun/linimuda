from datetime import date

from coderedcms.models import CoderedArticlePage, CoderedArticleIndexPage
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from website_insanq_project.apps.website.models import ReadOnlyPanel
from wagtail.utils.decorators import cached_classmethod


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

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["article.ArticleIndexPage"]
    subpage_types = []

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    # Panel

    # TODO -- Not needed to override right now, delete after accepted
    # bottom_content_panels = []

    # classify_panels = [
    #     FieldPanel("classifier_terms", widget=ClassifierSelectWidget()),
    #     FieldPanel("tags"),
    # ]

    # promote_panels = [
    #     MultiFieldPanel(
    #         [
    #             FieldPanel("slug"),
    #             FieldPanel("seo_title"),
    #             FieldPanel("search_description"),
    #             ImageChooserPanel("og_image"),
    #         ],
    #         _("Page Meta Data"),
    #     ),
    #     MultiFieldPanel(
    #         [
    #             HelpPanel(
    #                 heading=_("About Organization Structured Data"),
    #                 content=_(
    #                     """The fields below help define brand, contact, and storefront
    #                 information to search engines. This information should be filled out on
    #                 the site’s root page (Home Page). If your organization has multiple locations,
    #                 then also fill this info out on each location page using that particular
    #                 location’s info."""
    #                 ),
    #             ),
    #             FieldPanel("struct_org_type"),
    #             FieldPanel("struct_org_name"),
    #             ImageChooserPanel("struct_org_logo"),
    #             ImageChooserPanel("struct_org_image"),
    #             FieldPanel("struct_org_phone"),
    #             FieldPanel("struct_org_address_street"),
    #             FieldPanel("struct_org_address_locality"),
    #             FieldPanel("struct_org_address_region"),
    #             FieldPanel("struct_org_address_postal"),
    #             FieldPanel("struct_org_address_country"),
    #             FieldPanel("struct_org_geo_lat"),
    #             FieldPanel("struct_org_geo_lng"),
    #             StreamFieldPanel("struct_org_hours"),
    #             StreamFieldPanel("struct_org_actions"),
    #             FieldPanel("struct_org_extra_json"),
    #         ],
    #         _("Structured Data - Organization"),
    #     ),
    # ]

    # integration_panels = []

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


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    hits = models.IntegerField(default=0, editable=False)
    body = None

    # Panel

    # Override to not contain template form
    layout_panels = [
        MultiFieldPanel(
            [
                FieldPanel("index_show_subpages"),
                FieldPanel("index_num_per_page"),
                FieldPanel("index_order_by"),
                FieldPanel("index_classifiers", widget=forms.CheckboxSelectMultiple()),
            ],
            heading=_("Show Child Pages"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_images"),
                FieldPanel("show_captions"),
                FieldPanel("show_meta"),
                FieldPanel("show_preview_text"),
            ],
            heading=_("Child page display"),
        ),
    ]

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

    # Only allow ArticlePages beneath this page.
    subpage_types = ["article.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


# class ArticleIndexPage(CoderedArticleIndexPage):
#     """
#     Shows a list of article sub-pages.
#     """

#     class Meta:
#         verbose_name = "Article Landing Page"

#     # Override to specify custom index ordering choice/default.
#     index_query_pagemodel = "article.ArticlePage"

#     # Only allow ArticlePages beneath this page.
#     subpage_types = ["article.ArticlePage"]

#     template = "coderedcms/pages/article_index_page.html"
