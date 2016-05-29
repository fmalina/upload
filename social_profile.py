from allauth.socialaccount.models import SocialAccount
from upload.models import File
from upload.management.commands.sync_uploads import get_missing


def load_image(a):
    """Load social media profile image.
    """
    print(a.user.username.upper())

    if a.provider=='google':
        url = a.extra_data['picture']
        # handle empty
        if not url or '-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA' in url:
            return

    if a.provider=='facebook':
        url = 'http://graph.facebook.com/%s/picture?height=500' % a.extra_data['id']

    # Download image and save it on the advert.
    ad = a.user.ad_set.first()

    if ad and not ad.file_set.filter(alt='me'):
        f = File(fn='', alt='me', pos=99, ad=ad)
        f.save()
        get_missing(f, url=url)
        print(f.url())
        ad.save(staff=True)
    return ad


def bulk_load():
    for a in SocialAccount.objects.all():
        load_image(a)
