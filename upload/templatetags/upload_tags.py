from django.template import Library
from upload import app_settings

register = Library()


@register.filter
def absolute_url(path):
    return path.replace(app_settings.UPLOAD_MEDIA_ROOT, '/')
