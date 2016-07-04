"""Django allauth integration that can download social profile image
from Google and Facebook and save it on their first collection.
"""
from allauth.socialaccount.models import SocialAccount
from upload.models import File, get_collection_model
from upload.utils.download import get_missing_file

Col = get_collection_model()

FB_API = 'http://graph.facebook.com/'
GOOGLE_BLANKMAN_URLPART = '-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA'


def load_profile_image(account):
    """Load social media profile image.
    """
    a = account
    print(a.user.username.upper())

    if a.provider == 'google':
        url = a.extra_data['picture']
        if not url or GOOGLE_BLANKMAN_URLPART in url:
            return

    if a.provider == 'facebook':
        url = FB_API + '%s/picture?height=500' % a.extra_data['id']

    col = Col.objects.filter(user=a.user).first()
    if col and not col.file_set.filter(alt='me'):
        f = File(fn='', alt='me', pos=99, col=col)
        f.save()
        get_missing_file(f, url)
        print(f.url())
        col.save(staff=True)
    return col


def bulk_load():
    for account in SocialAccount.objects.all():
        load_profile_image(account)
