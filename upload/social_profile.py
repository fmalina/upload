"""Django allauth integration that can download social profile image
from Google and Facebook and save it on their first collection.
"""
from upload.utils.download import get_missing_file
from upload.models import File


FB_API = 'http://graph.facebook.com/'
GOOGLE_BLANKMAN_URLPART = '-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA'


def load_profile_image(account):
    """Load social media profile image.
    """
    a = account

    if a.provider == 'google':
        url = a.extra_data['picture']
        if not url or GOOGLE_BLANKMAN_URLPART in url:
            return

    if a.provider == 'facebook':
        url = FB_API + '%s/picture?height=500' % a.extra_data['id']

    f = File(fn='', alt='me', pos=99, col=None)
    f.save()
    get_missing_file(f, url)
    return f
