from django import template
import phonenumbers

register = template.Library()


@register.simple_tag
def format_phone(nomor):
    return phonenumbers.format_number(
        phonenumbers.parse(f"+{str(nomor)}", None),
        phonenumbers.PhoneNumberFormat.INTERNATIONAL,
    )
