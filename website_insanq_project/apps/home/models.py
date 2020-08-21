from coderedcms.models import CoderedWebPage
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
    MultiFieldPanel,
    FieldPanel,
    PageChooserPanel,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.blocks import PageChooserBlock
from website_insanq_project.apps.website.models import ReadOnlyPanel
from website_insanq_project.apps.article.models import ArticleIndexPage, ArticlePage
from website_insanq_project.apps.event.models import EventIndexPage, EventPage


class LayananBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    thumbnail = ImageChooserBlock()
    content = blocks.RichTextBlock(required=False)
    related_page = PageChooserBlock(required=False)


class HomePage(CoderedWebPage):
    class Meta:
        verbose_name = "Home"

    hits = models.IntegerField(default=0, editable=False)

    def add_hits(self):
        self.hits += 1
        self.save()
        return ""

    def get_context(self, request):
        context = super().get_context(request)
        context["recent_articles"] = []
        context["recent_events"] = []
        try:
            context["recent_articles"] = (
                ArticlePage.objects.child_of(self.landing_articles)
                .live()
                .order_by(self.landing_articles.index_order_by)[:3]
            )
            context["recent_events"] = (
                EventPage.objects.child_of(self.landing_events)
                .live()
                .order_by(self.landing_events.index_order_by)[:4]
            )
        except Exception as e:
            print(e)
        return context

    search_fields = []
    ###############
    # Panels
    ###############
    layout_panels = []
    settings_panels = Page.settings_panels
    body_content_panels = []
    # section layanan
    section_layanan = StreamField([("Layanan", LayananBlock())], blank=True)
    home_company_name = models.CharField(max_length=255, blank=True)
    home_description = models.CharField(max_length=1023, blank=True)
    home_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    landing_articles_title = models.CharField(max_length=255, blank=True)
    landing_articles = models.ForeignKey(
        ArticleIndexPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    landing_events_title = models.CharField(max_length=255, blank=True)
    landing_events = models.ForeignKey(
        EventIndexPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("home_company_name"),
                FieldPanel("home_description"),
                ImageChooserPanel("home_image"),
            ],
            _("Main Home"),
        ),
        StreamFieldPanel("section_layanan"),
        MultiFieldPanel(
            [
                FieldPanel("landing_articles_title"),
                PageChooserPanel("landing_articles"),
            ],
            _("Section Landing Articles"),
        ),
        MultiFieldPanel(
            [FieldPanel("landing_events_title"), PageChooserPanel("landing_events")],
            _("Section Landing Events"),
        ),
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

    parent_page_types = []
