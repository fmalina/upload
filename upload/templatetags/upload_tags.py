from django.template import Library
from django.conf import settings

register = Library()


@register.filter
def fixurl(path):
    """Fix common problems with easy_thumbnail generated thumbnail URLs
    """
    return path.replace(settings.STATIC_ROOT, '/')\
               .replace('media/media', 'media')
