from django.template import Library
from django.conf import settings

register = Library()


@register.filter
def fixurl(path):
    return path.replace(settings.STATIC_ROOT, '/')
