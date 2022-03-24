"""
Uploads backup utility

Sync down uploads referenced in the local database
that aren't present on the local disk.

Speed tips:
 - Set start to PK of the last synced file to save on local filesystem lookups.
 - Run 2nd terminal tab increasing the start to half way end.

$ ./manage.py sync_uploads [START_PK]
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from upload.utils.spoonfeed import spoonfeed
from upload.utils.download import get_missing_file
from upload.models import File


def get_missing_file_locally(file):
    url = 'https://' + settings.DOMAIN + file.url()
    get_missing_file(file, url)


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = 0
        if args:
            start = int(args[0])
        print(f"Syncing uploads from live to dev starting at PK:{start}.")
        if settings.DEBUG:
            spoonfeed(File.objects, get_missing_file_locally, start=start)
        else:
            print("Only run on local dev with DEBUG=True.")
