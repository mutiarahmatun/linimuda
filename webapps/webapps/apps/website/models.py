"""
Creatable pages used in CodeRed CMS.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage
)
from wagtail.admin.edit_handlers import (
    FieldPanel,
    EditHandler,
    StreamFieldPanel,
)

from wagtail.core import blocks
from wagtail.core.fields import StreamField



class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'
        ordering = ['-first_published_at']

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage']

    template = 'coderedcms/pages/article_index_page.html'


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'coderedcms/pages/form_page.html'


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """
    class Meta:
        ordering = ['sort_order']

    page = ParentalKey('FormPage', related_name='form_fields')


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """
    class Meta:
        verbose_name = 'Web Page'

    template = 'coderedcms/pages/web_page.html'

class PageLinkBlock(blocks.StructBlock):
    """
    A component of information with image, text, and buttons.
    """

    display_text = blocks.CharBlock(max_length=255)
    page = blocks.PageChooserBlock(required=False)
    external_url = blocks.URLBlock(
        required=False, help_text="External URL will be prioritized over page link"
    )

class BlockPageLinkBlock(blocks.StructBlock):
    display_text = blocks.CharBlock(max_length=255)
    sub_links = blocks.StreamBlock([("SubLink", PageLinkBlock())])

class Navbar(models.Model):
    class Meta:
        verbose_name = _("Navigation Bar")

    name = models.CharField(max_length=255)
    navigation_links = StreamField(
        [("NonDropdown", PageLinkBlock()), ("Dropdown", BlockPageLinkBlock())],
        blank=True,
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("navigation_links"),
    ]

    def __str__(self):
        return self.name