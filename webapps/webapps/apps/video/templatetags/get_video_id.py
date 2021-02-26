import re
from django import template

register = template.Library()


@register.filter
def get_video_id(value):

    regex = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})"
    )

    match = regex.match(value)

    if not match:
        return ""
    return match.group("id")
