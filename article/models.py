import datetime

from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class ArticlePage(Page):
    date = models.DateField("Post date", default=datetime.date.today)
    content = RichTextField(blank=True)
    coba = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("content", classname="full"),
    ]
