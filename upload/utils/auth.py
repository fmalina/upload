from django.conf import settings
from django.utils.http import urlquote
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_url(next_url, next_name=REDIRECT_FIELD_NAME):
    """ Use with care.
    There are no checks that the next_url had not been tampered with.
    """
    return '%s?%s=%s' % (settings.LOGIN_URL, next_name, urlquote(next_url))
