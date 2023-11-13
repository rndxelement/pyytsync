from django import template
from django.conf import settings

register = template.Library()

ALLOWED_SETTINGS = ['APP_VERSION']

@register.simple_tag
def get_setting(name):
    if name in ALLOWED_SETTINGS:
        return getattr(settings, name, "")
    return ""
