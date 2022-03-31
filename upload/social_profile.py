"""
Django allauth integration that can download social profile image
from Google and Facebook. Use in post signup callbacks etc.
"""
from upload.utils.download import get_missing_file
from upload.models import File


FB_API = 'http://graph.facebook.com/'
GOOGLE_BLANKMAN_URLPART = '-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA'


def load_profile_image(account):
    """Load social media profile image"""
    if account.provider == 'google':
        url = account.extra_data['picture']
        # don't download the dreadful default Google profile picture
        if not url or GOOGLE_BLANKMAN_URLPART in url:
            return

    if account.provider == 'facebook':
        account_id = account.extra_data['id']
        url = f"{FB_API}{account_id}/picture?height=500"

    f = File(fn='', alt='me', pos=99, col=None)
    f.save()
    get_missing_file(f, url)
    return f
