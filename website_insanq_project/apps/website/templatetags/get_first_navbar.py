from django import template
from website_insanq_project.apps.website.models import Navbar

register = template.Library()


@register.simple_tag
def get_first_navbar():
    return Navbar.objects.first()
